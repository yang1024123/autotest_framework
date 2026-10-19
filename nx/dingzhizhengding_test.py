"""定值上送情况统计测试（nx 模块）。

查询数据库并导出 Excel 报表。公共逻辑已抽取为辅助函数，
数据库连接通过全局 db_cursor fixture 管理，避免重复连接与资源泄漏。
"""

import allure
import xlsxwriter as xw


# ---------------------------------------------------------------------------
# 公共查询辅助
# ---------------------------------------------------------------------------
def get_factory_names(cursor):
    """获取满足条件的厂家名称列表。"""
    sql = """
        SELECT PRODUCT_FACTORY
        FROM DIM_MOD_DEVICE
        WHERE TYPE = 1
          AND LINE_ID IN (SELECT LINE_ID FROM DIM_MOD_LINE)
          AND AREA_INFO IN (SELECT ORG_ID FROM DIM_MOD_ORG WHERE org_level = 3)
          AND FIXED_VALUE_TERMINAL IN ('1', '2')
        GROUP BY PRODUCT_FACTORY
    """
    cursor.execute(sql)
    return [row["PRODUCT_FACTORY"] for row in cursor.fetchall()]


def get_device_counts(cursor, terminal_values):
    """按厂家统计设备数（参数化 FIXED_VALUE_TERMINAL 条件，避免 SQL 拼接）。"""
    placeholders = ",".join(["%s"] * len(terminal_values))
    sql = f"""
        SELECT PRODUCT_FACTORY, COUNT(*) AS cnt
        FROM DIM_MOD_DEVICE
        WHERE FIXED_VALUE_TERMINAL IN ({placeholders})
          AND TYPE = 1
          AND LINE_ID IN (SELECT LINE_ID FROM DIM_MOD_LINE)
          AND AREA_INFO IN (SELECT ORG_ID FROM DIM_MOD_ORG WHERE org_level = 3)
        GROUP BY PRODUCT_FACTORY
    """
    cursor.execute(sql, terminal_values)
    return {row["PRODUCT_FACTORY"]: row["cnt"] for row in cursor.fetchall()}


# 地市列表（多处复用，集中定义）
AREAS = ["吴忠", "青铜峡", "红寺堡", "同心", "利通区"]
AREAS_ALL = ["总数", "宁东", "石嘴山", "吴忠", "中卫", "固原", "银川"]


def _area_case_sql(org_path_field="ORG_NAME", like_field="ORG_NAME"):
    """生成按地市统计的 CASE WHEN SQL 片段。"""
    parts = []
    for area in AREAS:
        parts.append(f"COUNT(CASE WHEN org.{like_field} LIKE '%{area}%' THEN 1 END) AS {area}")
    return ",\n".join(parts)


# ---------------------------------------------------------------------------
# 测试用例
# ---------------------------------------------------------------------------
@allure.feature("定值厂家定值上送情况")
def test_factory(db_cursor):
    file_path = "nx/厂家定值上送情况.xlsx"
    workbook = xw.Workbook(file_path)
    worksheet = workbook.add_worksheet("sheet1")
    title = ["厂家名称", "设备数", "上送定值终端数", "定值上送率"]
    worksheet.write_row("A1", title)

    factory_names = get_factory_names(db_cursor)
    total_devices = get_device_counts(db_cursor, ("1", "2"))
    uploaded_devices = get_device_counts(db_cursor, ("2",))

    row_idx = 1
    for factory in factory_names:
        worksheet.write(row_idx, 0, factory)
        dev_count = total_devices.get(factory, 0)
        up_count = uploaded_devices.get(factory, 0)
        worksheet.write(row_idx, 1, dev_count)
        worksheet.write(row_idx, 2, up_count)
        rate = (up_count / dev_count * 100) if dev_count > 0 else 0
        worksheet.write(row_idx, 3, f"{rate:.2f}%")
        row_idx += 1
    workbook.close()


@allure.feature("省市定值上送情况")
def test_provinceAndcity(db_cursor):
    file_path = "nx/省市定值上送情况.xlsx"
    workbook = xw.Workbook(file_path)
    worksheet = workbook.add_worksheet("sheet1")
    title = ["地市", "馈线", "上送定值馈线", "终端", "上送定值终端"]
    worksheet.write_row("A1", title)

    for row, area in enumerate(AREAS, start=1):
        worksheet.write(row, 0, area)

    queries = [
        {
            "sql": f"""
                SELECT {_area_case_sql()}
                FROM DIM_MOD_ORG org, DIM_MOD_LINE ff
                WHERE ff.AREA_INFO = org.org_id AND org.org_level = 3
            """,
            "col_offset": 1,
        },
        {
            "sql": f"""
                SELECT {_area_case_sql()}
                FROM DIM_MOD_ORG org, DIM_MOD_LINE ff
                WHERE ff.AREA_INFO = org.org_id
                  AND ff.LINE_ID IN (
                      SELECT DISTINCT LINE_ID FROM DIM_MOD_DEVICE
                      WHERE FIXED_VALUE_TERMINAL IN ('2')
                  )
                  AND org.org_level = 3
            """,
            "col_offset": 2,
        },
    ]

    for query_info in queries:
        db_cursor.execute(query_info["sql"])
        results = db_cursor.fetchall()
        if results:
            col_values = [value for row in results for value in row.values()]
            for row, value in enumerate(col_values, start=1):
                worksheet.write(row, query_info["col_offset"], value)
    workbook.close()


@allure.feature("省市定值单上送情况")
def test_orederTotal(db_cursor):
    file_path = "nx/省市定值单上送情况.xlsx"
    workbook = xw.Workbook(file_path)
    worksheet = workbook.add_worksheet("sheet1")

    headers = ["地市", "定值单总数", "审批中", "审批完成", "已驳回", "下发完成", "校核完成", "已归档", "审批通过"]
    worksheet.write_row("A1", headers)

    for row_idx, area in enumerate(AREAS_ALL, start=1):
        worksheet.write(row_idx, 0, area)

    queries = [
        ("", 1),
        ("AND ff.STATUS in ('1')", 2),
        ("AND ff.STATUS in ('2','3')", 3),
        ("AND ff.STATUS in ('3')", 4),
        ("AND ff.STATUS in ('401','402')", 5),
        ("AND ff.STATUS in ('501','502')", 6),
        ("AND ff.STATUS in ('600')", 7),
        ("AND ff.STATUS in ('2')", 8),
    ]

    for condition, col_idx in queries:
        sql = f"""
            SELECT {_area_case_sql(like_field="ORG_PATH")}
            FROM DIM_MOD_ORG org, ORDER_FIXED_VAL_TUNING ff
            WHERE ff.org_id = org.org_id {condition}
        """
        db_cursor.execute(sql)
        result = db_cursor.fetchone()
        if result:
            row_idx = 1
            for value in result.values():
                worksheet.write(row_idx, col_idx, value)
                row_idx += 1
    workbook.close()


@allure.feature("定值异动统计")
def test_abnormalTotal(db_cursor):
    file_path = "nx/定值异动统计.xlsx"
    workbook = xw.Workbook(file_path)
    worksheet = workbook.add_worksheet("sheet1")
    title = ["地市", "定值异动", "FTU定值异动", "DTU定值异动"]
    worksheet.write_row("A1", title)

    for row, area in enumerate(AREAS_ALL, start=1):
        worksheet.write(row, 0, area)

    # 三组查询仅 TYPE 条件不同：全部 / '1'(FTU) / '2'(DTU)
    conditions = [("('1','2')", 1), ("'1'", 2), ("'2'", 3)]
    for type_cond, col_idx in conditions:
        sql = f"""
            SELECT {_area_case_sql(like_field="ORG_PATH")}
            FROM DIM_MOD_ORG org
            JOIN DIM_MOD_DEVICE DD ON DD.AREA_INFO = org.org_id
            JOIN DIM_DEVICE_ABNORMAL ff ON DD.device_id = ff.DEVICE_ID AND DD.TYPE IN ({type_cond})
        """
        db_cursor.execute(sql)
        results = db_cursor.fetchall()
        values = [value for row in results for value in row.values()]
        for row, value in enumerate(values, start=1):
            worksheet.write(row, col_idx, value)
    workbook.close()
