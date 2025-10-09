import os

import pytest

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pytest.main(['-s', '--clean-alluredir', '--alluredir=allure-results'])
    os.system(r"allure generate -c -o allure-report")