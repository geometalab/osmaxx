def pytest_addoption(parser):
    parser.addoption("--runslow", action="store_true",
                     help="run slow tests")
    parser.addoption("--all-utm-zones", action="store_true",
                     help="run tests parametrized with an UTM zone for all 120 UTM zones")
