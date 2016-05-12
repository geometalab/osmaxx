def pytest_addoption(parser):
    parser.addoption("--runslow", action="store_true",
                     help="run slow tests")
    parser.addoption("--selenium", action="store_true",
                     help="run selenium tests")
