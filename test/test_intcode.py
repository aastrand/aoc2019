import unittest

from intcode import decode_instruction, create_runner, NotInitializedException


class IntCodeTest(unittest.TestCase):

    def test_decode_instruction(self):
        self.assertEquals((1, (0, 1, 0)), decode_instruction(1001))
        self.assertEquals((1, (1, 0, 0)), decode_instruction(101))
        self.assertEquals((2, (0, 0, 0)), decode_instruction(2))
        self.assertEquals((99, (0, 0, 0)), decode_instruction(99))
        self.assertEquals((7, (1, 1, 2)), decode_instruction(21107))

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

    def test_large_numbers(self):
        runner = create_runner("test/large_numbers.txt")
        runner.run()
        self.assertEquals(1219070632396864, runner.output_value())

        runner = create_runner("test/large_numbers2.txt")
        runner.run()
        self.assertEquals(1125899906842624, runner.output_value())

    def test_rel_base(self):
        runner = create_runner("test/rel_base.txt")
        runner.run()
        self.assertEquals(19, runner._rel_base)

        runner = create_runner("test/rel_base2.txt")
        runner.run()
        self.assertEquals(31337, runner.output_value())

    def test_expand_memory(self):
        runner = create_runner("test/expand_memory_store.txt")
        runner.run()
        self.assertEquals(8, runner.output_value())
        self.assertEquals(11, len(runner._program))

        runner = create_runner("test/expand_memory_load.txt")
        runner.run()
        self.assertEquals(81, runner.output_value())
        self.assertEquals(101, len(runner._program))

    def test_quine(self):
        runner = create_runner("test/quine.txt")
        output = []
        while True:
            if runner.run(True) == 99:
                break;
            output.append(runner.output_value())

        self.assertEquals(output, runner._program[:16])

    def test_rel_store(self):
        runner = create_runner("test/rel_store.txt", 31337)
        runner.run()
        self.assertEquals(31337, runner.output_value())

    def test_rel_equals(self):
        runner = create_runner("test/rel_equals.txt")
        runner.run()
        self.assertEquals(1, runner.output_value())

    def test_rel_less_than(self):
        runner = create_runner("test/rel_lt.txt")
        runner.run()
        self.assertEquals(1, runner.output_value())

    def test_rel_add(self):
        runner = create_runner("test/rel_add.txt")
        runner.run()
        self.assertEquals(22202, runner.output_value())

    def test_rel_add(self):
        runner = create_runner("test/rel_mul.txt")
        runner.run()
        self.assertEquals(222020, runner.output_value())

    def test_rel_jump(self):
        runner = create_runner("test/rel_jump.txt")
        runner.run()
        self.assertEquals(31337, runner.output_value())

    def test_rel_jnz(self):
        runner = create_runner("test/rel_jnz.txt")
        runner.run()
        self.assertEquals(31337, runner.output_value())

    def test_reset_input_offet(self):
        runner = create_runner("test/io2.txt", 1, 2)
        runner.run()
        out = runner.output_value()
        runner.set_input_values(2, 1)
        runner._pc = 0
        runner.run(True)
        self.assertEquals(2, runner.output_value())

    def test_breakpoint_on_opcodes(self):
        runner = create_runner("test/io.txt", 1)
        ec = runner.run()
        self.assertEquals(99, ec)

        runner = create_runner("test/io.txt", 1)
        runner.add_breakpoint_opcode(4)
        runner.add_breakpoint_opcode(3)
        ec = runner.run()
        self.assertEquals(3, ec)
        ec = runner.run()
        self.assertEquals(4, ec)
        self.assertEquals(1, runner.output_value())
