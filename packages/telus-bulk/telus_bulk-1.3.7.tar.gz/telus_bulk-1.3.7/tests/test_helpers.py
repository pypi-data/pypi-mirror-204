from telus_bulk.helpers.mutiple_spaces import str_to_single_space


class TestHelpers:
    def test_str_to_single_space(self):
        test_address = "    418   A Weird  Street    Name    "
        print(str_to_single_space(test_address))
        assert str_to_single_space(test_address) == "418 A Weird Street Name"
