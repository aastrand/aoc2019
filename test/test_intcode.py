import unittest

from intcode import decode_instruction, create_runner, NotInitializedException


class IntCodeTest(unittest.TestCase):

    def test_decode_instruction(self):
        self.assertEquals((1, 0, 1), decode_instruction(1001))
        self.assertEquals((1, 1, 0), decode_instruction(101))
        self.assertEquals((2, 0, 0), decode_instruction(2))
        self.assertEquals((99, 0, 0), decode_instruction(99))

    def test_output_value(self):
        runner = create_runner("test/equal_8_pos_mode.txt", 8)
        try:
            val = runner.output_value()
            self.fail("Should raise NotInitializedException")
        except NotInitializedException:
            pass

    def test_equal_8_int_mode(self):
        runner = create_runner("test/equal_8_int_mode.txt", 8)
        runner.run()
        self.assertEquals(1, runner.output_value())

        runner = create_runner("test/equal_8_int_mode.txt", 1)
        runner.run()
        self.assertEquals(0, runner.output_value())

    def test_equal_8_pos_mode(self):
        runner = create_runner("test/equal_8_pos_mode.txt", 8)
        runner.run()
        self.assertEquals(1, runner.output_value())

        runner = create_runner("test/equal_8_pos_mode.txt", 1)
        runner.run()
        self.assertEquals(0, runner.output_value())

    def test_less_than_8_int_mode(self):
        runner = create_runner("test/less_than_8_int_mode.txt", 1)
        runner.run()
        self.assertEquals(1, runner.output_value())

        runner = create_runner("test/less_than_8_int_mode.txt", 8)
        runner.run()
        self.assertEquals(0, runner.output_value())

    def test_less_than_8_pos_mode(self):
        runner = create_runner("test/less_than_8_pos_mode.txt", 1)
        runner.run()
        self.assertEquals(1, runner.output_value())

        runner = create_runner("test/less_than_8_pos_mode.txt", 8)
        runner.run()
        self.assertEquals(0, runner.output_value())

    def test_jump_int(self):
        runner = create_runner("test/jump_int.txt", 1)
        runner.run()
        self.assertEquals(1, runner.output_value())

        runner = create_runner("test/jump_int.txt", 0)
        runner.run()
        self.assertEquals(0, runner.output_value())

    def test_jump_pos(self):
        runner = create_runner("test/jump_pos.txt", 1)
        runner.run()
        self.assertEquals(1, runner.output_value())

        runner = create_runner("test/jump_pos.txt", 0)
        runner.run()
        self.assertEquals(0, runner.output_value())

    def test_io(self):
        runner = create_runner("test/io.txt", 31337)
        runner.run()
        self.assertEquals(31337, runner.output_value())
