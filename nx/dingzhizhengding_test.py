import pymysql
import xlsxwriter as xw
import allure
def get_factory_names(cursor):
    base_query = """
        SELECT PRODUCT_FACTORY
        FROM DIM_MOD_DEVICE 
        WHERE TYPE = 1
        AND LINE_ID IN (SELECT LINE_ID FROM DIM_MOD_LINE) 
        AND AREA_INFO IN (SELECT ORG_ID FROM DIM_MOD_ORG WHERE org_level = 3)
        AND FIXED_VALUE_TERMINAL IN ('1','2') 
        GROUP BY PRODUCT_FACTORY
    """
    cursor.execute(base_query)
    return [row['PRODUCT_FACTORY'] for row in cursor.fetchall()]



def get_device_counts(cursor, condition):
    query = f"""
        SELECT PRODUCT_FACTORY, COUNT(*) as cnt
        FROM DIM_MOD_DEVICE 
        WHERE FIXED_VALUE_TERMINAL {condition}
        AND TYPE = 1
        AND LINE_ID IN (SELECT LINE_ID FROM DIM_MOD_LINE) 
        AND AREA_INFO IN (SELECT ORG_ID FROM DIM_MOD_ORG WHERE org_level = 3)
        GROUP BY PRODUCT_FACTORY
    """
    cursor.execute(query)
    return {row['PRODUCT_FACTORY']: row['cnt'] for row in cursor.fetchall()}
@allure.feature("定值厂家定值上送情况")
def test_factory(parse_db_config):
    connection = None
    cursor = None
    workbook = None
    file_path = "nx/厂家定值上送情况.xlsx"
    try:
        connection = pymysql.connect(**parse_db_config)
        cursor = connection.cursor()


        workbook = xw.Workbook(file_path)
        worksheet = workbook.add_worksheet("sheet1")
        title = ['厂家名称', '设备数', '上送定值终端数', '定值上送率']
        worksheet.write_row('A1', title)


        factory_names = get_factory_names(cursor)
        total_devices = get_device_counts(cursor, "IN ('1','2')")
        uploaded_devices = get_device_counts(cursor, "IN ('2')")


        row_idx = 1
        for factory in factory_names:
            worksheet.write(row_idx, 0, factory)
            dev_count = total_devices.get(factory, 0)
            worksheet.write(row_idx, 1, dev_count)
            up_count = uploaded_devices.get(factory, 0)
            worksheet.write(row_idx, 2, up_count)
            rate = (up_count / dev_count * 100) if dev_count > 0 else 0
            worksheet.write(row_idx, 3, f"{rate:.2f}%")
            row_idx += 1
        workbook.close()
    except pymysql.MySQLError as e:
        print(f"数据库错误：{e}")
    except Exception as e:
        print(f"发生未知错误：{e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
@allure.feature("省市定值上送情况")
def test_provinceAndcity(parse_db_config):
    connection = None
    workbook = None
    file_path = "nx/省市定值上送情况.xlsx"
    try:
        connection = pymysql.connect(**parse_db_config)
        cursor = connection.cursor()

        # 创建Excel工作簿
        workbook = xw.Workbook(file_path)
        worksheet1 = workbook.add_worksheet("sheet1")
        worksheet1.activate()
        title = ['地市', '馈线', '上送定值馈线', '终端', '上送定值终端']
        worksheet1.write_row('A1', title)

        # 定义查询和对应的列名
        queries = [
            {
                "sql": """
                    SELECT 
                        COUNT(CASE WHEN org.ORG_NAME LIKE '%吴忠%' THEN 1 END) AS 吴忠,
                        COUNT(CASE WHEN org.ORG_NAME LIKE '%青铜峡%' THEN 1 END) AS 青铜峡,
                        COUNT(CASE WHEN org.ORG_NAME LIKE '%红寺堡%' THEN 1 END) AS 红寺堡,
                        COUNT(CASE WHEN org.ORG_NAME LIKE '%同心%' THEN 1 END) AS 同心,
                        COUNT(CASE WHEN org.ORG_NAME LIKE '%利通%' THEN 1 END) AS 利通区
                    FROM DIM_MOD_ORG org, DIM_MOD_LINE ff 
                    WHERE ff.AREA_INFO = org.org_id
                    AND org.org_level = 3
                """,
                "col_offset": 1
            },
            {
                "sql": """
                    SELECT 
                        COUNT(CASE WHEN org.ORG_NAME LIKE '%吴忠%' THEN 1 END) AS 吴忠,
                        COUNT(CASE WHEN org.ORG_NAME LIKE '%青铜峡%' THEN 1 END) AS 青铜峡,
                        COUNT(CASE WHEN org.ORG_NAME LIKE '%红寺堡%' THEN 1 END) AS 红寺堡,
                        COUNT(CASE WHEN org.ORG_NAME LIKE '%同心%' THEN 1 END) AS 同心,
                        COUNT(CASE WHEN org.ORG_NAME LIKE '%利通%' THEN 1 END) AS 利通区
                    FROM DIM_MOD_ORG org, DIM_MOD_LINE ff 
                    WHERE ff.AREA_INFO = org.org_id 
                    AND ff.LINE_ID IN (SELECT DISTINCT LINE_ID FROM DIM_MOD_DEVICE WHERE FIXED_VALUE_TERMINAL in ('2'))
                    AND org.org_level = 3
                """,
                "col_offset": 2
            },
        ]

        # 写入地区名称
        areas = ['吴忠', '青铜峡', '红寺堡', '同心', '利通区']
        for row, area in enumerate(areas, start=1):
            worksheet1.write(row, 0, area)

        # 执行查询并写入结果
        for query_info in queries:
            cursor.execute(query_info["sql"])
            results = cursor.fetchall()

            if results:
                # 更安全的查询结果处理
                col_values = []
                for row in results:
                    for value in row.values():
                        col_values.append(value)

                for row, value in enumerate(col_values, start=1):
                    worksheet1.write(row, query_info["col_offset"], value)

        connection.commit()
        workbook.close()
        cursor.close()
        connection.close()

    except pymysql.MySQLError as e:
        print(f"数据库错误：{e}")
        if connection:
            connection.rollback()
    except Exception as e:
        print(f"发生未知错误：{e}")
    finally:
        if connection and not connection.open:
            try:
                connection.close()
            except:
                pass

@allure.feature("省市定值单上送情况")
def test_orederTotal(parse_db_config):
    connection = None
    cursor = None
    workbook = None
    file_path = "nx/省市定值单上送情况.xlsx"
    try:
        connection = pymysql.connect(**parse_db_config)
        cursor = connection.cursor()

        # 创建Excel工作簿
        workbook = xw.Workbook(file_path)
        worksheet1 = workbook.add_worksheet("sheet1")
        worksheet1.activate()

        # 表头和地区列表
        headers = ['地市', '定值单总数', '审批中', '审批完成', '已驳回', '下发完成', '校核完成', '已归档', '审批通过']
        areas = ['总数', '宁东', '石嘴山', '吴忠', '中卫', '固原', '银川', '青铜峡', '红寺堡', '同心', '利通区']

        worksheet1.write_row('A1', headers)

        # 写入地区名称列
        for row_idx, area in enumerate(areas, start=1):
            worksheet1.write(row_idx, 0, area)

        # 定义查询条件和列映射
        queries = [
            ("", 1),  # 总查询
            ("AND ff.STATUS in ('1')", 2),  # 审批中
            ("AND ff.STATUS in ('2','3')", 3),  # 审批完成
            ("AND ff.STATUS in ('3')", 4),  # 已驳回
            ("AND ff.STATUS in ('401','402')", 5),  # 下发完成
            ("AND ff.STATUS in ('501','502')", 6),  # 校核完成
            ("AND ff.STATUS in ('600')", 7),  # 已归档
            ("AND ff.STATUS in ('2')", 8)  # 审批通过
        ]

        base_sql = """
                    SELECT 
                        COUNT(CASE WHEN org.ORG_PATH LIKE '%宁夏%' THEN 1 END) AS 总数,
                        COUNT(CASE WHEN org.ORG_PATH LIKE '%宁东%' THEN 1 END) AS 宁东,
                        COUNT(CASE WHEN org.ORG_PATH LIKE '%石嘴山%' THEN 1 END) AS 石嘴山,
                        COUNT(CASE WHEN org.ORG_PATH LIKE '%吴忠%' THEN 1 END) AS 吴忠,
                        COUNT(CASE WHEN org.ORG_PATH LIKE '%中卫%' THEN 1 END) AS 中卫,
                        COUNT(CASE WHEN org.ORG_PATH LIKE '%固原%' THEN 1 END) AS 固原,
                        COUNT(CASE WHEN org.ORG_PATH LIKE '%银川%' THEN 1 END) AS 银川,
                        COUNT(CASE WHEN org.ORG_PATH LIKE '%青铜峡%' THEN 1 END) AS 青铜峡,
                        COUNT(CASE WHEN org.ORG_PATH LIKE '%红寺堡%' THEN 1 END) AS 红寺堡,
                        COUNT(CASE WHEN org.ORG_PATH LIKE '%同心%' THEN 1 END) AS 同心,
                        COUNT(CASE WHEN org.ORG_PATH LIKE '%利通%' THEN 1 END) AS 利通区
                    FROM DIM_MOD_ORG org, ORDER_FIXED_VAL_TUNING ff 
                    WHERE ff.org_id = org.org_id
                """

        # 执行查询并写入Excel
        for condition, col_idx in queries:
            sql = base_sql + condition
            cursor.execute(sql)
            result = cursor.fetchone()

            if result:
                row_idx = 1  # 从第二行开始写入数据
                for value in result.values():
                    worksheet1.write(row_idx, col_idx, value)
                    row_idx += 1

        workbook.close()

    except pymysql.MySQLError as e:
        print(f"数据库错误：{e}")
    except Exception as e:
        print(f"发生未知错误：{e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        if workbook:
            # workbook.close() 已在前面调用
            pass
@allure.feature("定值异动统计")
def test_abnormalTotal(parse_db_config):
    connection = None
    cursor = None
    workbook = None
    file_path = "nx/定值异动统计.xlsx"
    try:
        connection = pymysql.connect(**parse_db_config)
        cursor = connection.cursor()

        # 创建Excel工作簿
        workbook = xw.Workbook(file_path)  # 创建工作簿
        worksheet1 = workbook.add_worksheet("sheet1")  # 创建子表
        worksheet1.activate()
        title = ['地市', '定值异动', 'FTU定值异动', 'DTU定值异动']  # 设置表头
        worksheet1.write_row('A1', title)  # 从A1单元格开始写入表头

        # SQL查询语句
        sql = """
        SELECT 
            COUNT(CASE WHEN org.ORG_PATH LIKE '%宁夏%' THEN 1 END) AS 总数,
            COUNT(CASE WHEN org.ORG_PATH LIKE '%宁东%' THEN 1 END) AS 宁东,
            COUNT(CASE WHEN org.ORG_PATH LIKE '%石嘴山%' THEN 1 END) AS 石嘴山,
            COUNT(CASE WHEN org.ORG_PATH LIKE '%吴忠%' THEN 1 END) AS 吴忠,
            COUNT(CASE WHEN org.ORG_PATH LIKE '%中卫%' THEN 1 END) AS 中卫,
            COUNT(CASE WHEN org.ORG_PATH LIKE '%固原%' THEN 1 END) AS 固原,
            COUNT(CASE WHEN org.ORG_PATH LIKE '%银川%' THEN 1 END) AS 银川
        FROM DIM_MOD_ORG org
        JOIN DIM_MOD_DEVICE DD ON DD.AREA_INFO = org.org_id
        JOIN DIM_DEVICE_ABNORMAL ff ON DD.device_id = ff.DEVICE_ID AND DD.TYPE in ('1','2'); 
                """

        # 原代码中的 SQL 查询和结果获取部分保持不变
        cursor.execute(sql)
        results = cursor.fetchall()  # 更改变量名为 results 以避免混淆

        # 提取每个字典的值并打印
        if results:
            # 如果有多行数据，提取所有行的值
            values1 = [tuple(row.values()) for row in results]
        else:
            print("无查询结果")

        sql_1 = """
        SELECT 
            COUNT(CASE WHEN org.ORG_PATH LIKE '%宁夏%' THEN 1 END) AS 总数,
            COUNT(CASE WHEN org.ORG_PATH LIKE '%宁东%' THEN 1 END) AS 宁东,
            COUNT(CASE WHEN org.ORG_PATH LIKE '%石嘴山%' THEN 1 END) AS 石嘴山,
            COUNT(CASE WHEN org.ORG_PATH LIKE '%吴忠%' THEN 1 END) AS 吴忠,
            COUNT(CASE WHEN org.ORG_PATH LIKE '%中卫%' THEN 1 END) AS 中卫,
            COUNT(CASE WHEN org.ORG_PATH LIKE '%固原%' THEN 1 END) AS 固原,
            COUNT(CASE WHEN org.ORG_PATH LIKE '%银川%' THEN 1 END) AS 银川
        FROM DIM_MOD_ORG org
        JOIN DIM_MOD_DEVICE DD ON DD.AREA_INFO = org.org_id
        JOIN DIM_DEVICE_ABNORMAL ff ON DD.device_id = ff.DEVICE_ID AND DD.TYPE = '1' 
                """

        # 原代码中的 SQL 查询和结果获取部分保持不变
        cursor.execute(sql_1)
        results = cursor.fetchall()  # 更改变量名为 results 以避免混淆

        # 提取每个字典的值并打印
        if results:
            # 如果有多行数据，提取所有行的值
            values2 = [tuple(row.values()) for row in results]
        else:
            print("无查询结果")

        sql_2 = """
        SELECT 
            COUNT(CASE WHEN org.ORG_PATH LIKE '%宁夏%' THEN 1 END) AS 总数,
            COUNT(CASE WHEN org.ORG_PATH LIKE '%宁东%' THEN 1 END) AS 宁东,
            COUNT(CASE WHEN org.ORG_PATH LIKE '%石嘴山%' THEN 1 END) AS 石嘴山,
            COUNT(CASE WHEN org.ORG_PATH LIKE '%吴忠%' THEN 1 END) AS 吴忠,
            COUNT(CASE WHEN org.ORG_PATH LIKE '%中卫%' THEN 1 END) AS 中卫,
            COUNT(CASE WHEN org.ORG_PATH LIKE '%固原%' THEN 1 END) AS 固原,
            COUNT(CASE WHEN org.ORG_PATH LIKE '%银川%' THEN 1 END) AS 银川
        FROM DIM_MOD_ORG org
        JOIN DIM_MOD_DEVICE DD ON DD.AREA_INFO = org.org_id
        JOIN DIM_DEVICE_ABNORMAL ff ON DD.device_id = ff.DEVICE_ID AND DD.TYPE = '2' 
                """

        # 原代码中的 SQL 查询和结果获取部分保持不变
        cursor.execute(sql_2)
        results = cursor.fetchall()  # 更改变量名为 results 以避免混淆

        # 提取每个字典的值并打印
        if results:
            # 如果有多行数据，提取所有行的值
            values3 = [tuple(row.values()) for row in results]
        else:
            print("无查询结果")

        g = 1
        area_info = ['总数', '宁东', '石嘴山', '吴忠', '中卫', '固原', '银川']
        for h in area_info:
            worksheet1.write(g, 0, h)
            g += 1

        a = 1
        for b in values1:
            for c in b:
                worksheet1.write(a, 1, c)
                a += 1

        d = 1
        for e in values2:
            for f in e:
                worksheet1.write(d, 2, f)
                d += 1

        i = 1
        for j in values3:
            for k in j:
                worksheet1.write(i, 3, k)
                i += 1

        workbook.close()  # 关闭表

        cursor.close()
        connection.close()

    except pymysql.MySQLError as e:
        print(f"数据库错误：{e}")
    except Exception as e:
        print(f"发生未知错误：{e}")