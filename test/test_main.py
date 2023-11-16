

from unittest import TestCase

from src.start_compiler import start_compiler


# It's a class that inherits from the TestCase class, and it's called Test
class Test(TestCase):

    def test_operation(self):
        """
        It tests the operation of the function.
        """
        code = start_compiler("../sample_input/operation.swift")
        self.assertEqual(
            """0 INT 0 3
1 INT 0 1
2 LIT 0 555
3 STO 0 3
4 RET 0 0
""", code, "operation")

    def test_declaration(self):
        """
        It tests the declaration of a variable.
        """
        code = start_compiler("../sample_input/declaration.swift")
        self.assertEqual("""0 INT 0 3
1 INT 0 1
2 LIT 0 555
3 STO 0 3
4 INT 0 1
5 LOD 0 3
6 LIT 0 10
7 OPR 0 2
8 STO 0 4
9 RET 0 0
""", code, "operation")

    def test_operators(self):
        """
        It tests the operators
        """
        code = start_compiler("../sample_input/operators.swift")
        self.assertEqual("""0 INT 0 3
1 INT 0 1
2 LIT 0 40
3 STO 0 3
4 INT 0 1
5 LIT 0 230
6 LOD 0 3
7 OPR 0 3
8 STO 0 4
9 INT 0 1
10 LIT 0 60
11 STO 0 5
12 RET 0 0
""", code, "operators")

    def test_if(self):
        """
        It tests if the
        condition is true.
        """
        code = start_compiler("../sample_input/if.swift")
        self.assertEqual("""0 INT 0 3
1 INT 0 1
2 LIT 0 0
3 STO 0 3
4 LIT 0 52
5 LIT 0 43
6 OPR 0 12
7 JMC 0 12
8 LIT 0 32
9 LOD 0 3
10 OPR 0 4
11 STO 0 3
12 RET 0 0
""", code, "if")

    def test_if_and(self):
            code = start_compiler("../sample_input/if_and.swift")
            self.assertEqual("""0 INT 0 3
1 INT 0 1
2 LIT 0 1
3 STO 0 3
4 LOD 0 3
5 LIT 0 5
6 OPR 0 10
7 JMC 0 20
8 LIT 0 52
9 LIT 0 43
10 OPR 0 12
11 JMC 0 20
12 LOD 0 3
13 LIT 0 5
14 OPR 0 12
15 JMC 0 20
16 LIT 0 32
17 LOD 0 3
18 OPR 0 4
19 STO 0 3
20 RET 0 0
""", code, "if_and")

    def test_if_and_or(self):
            code = start_compiler("../sample_input/if_and_or.swift")
            self.assertEqual("""0 INT 0 3
1 INT 0 1
2 LIT 0 1
3 STO 0 3
4 LOD 0 3
5 LIT 0 5
6 OPR 0 12
7 LIT 0 -1
8 OPR 0 2
9 JMC 0 18
10 LIT 0 52
11 LIT 0 43
12 OPR 0 12
13 JMC 0 22
14 LOD 0 3
15 LIT 0 5
16 OPR 0 10
17 JMC 0 22
18 LIT 0 32
19 LOD 0 3
20 OPR 0 4
21 STO 0 3
22 RET 0 0
""", code, "if_and_or")

    def test_if_or(self):
            code = start_compiler("../sample_input/if_or.swift")
            self.assertEqual("""0 INT 0 3
1 INT 0 1
2 LIT 0 1
3 STO 0 3
4 LOD 0 3
5 LIT 0 5
6 OPR 0 12
7 LIT 0 -1
8 OPR 0 2
9 JMC 0 20
10 LIT 0 52
11 LIT 0 43
12 OPR 0 12
13 LIT 0 -1
14 OPR 0 2
15 JMC 0 20
16 LIT 0 1
17 LIT 0 1
18 OPR 0 12
19 JMC 0 24
20 LIT 0 32
21 LOD 0 3
22 OPR 0 4
23 STO 0 3
24 RET 0 0
""", code, "if_or")

    def test_bool(self):
        code = start_compiler("../sample_input/bool.swift")
        self.assertEqual("""0 INT 0 3
1 INT 0 1
2 LIT 0 1
3 STO 0 3
4 INT 0 1
5 LIT 0 0
6 STO 0 4
7 LOD 0 4
8 JMC 0 12
9 INT 0 1
10 LIT 0 9000
11 STO 0 5
12 LOD 0 3
13 JMC 0 17
14 INT 0 1
15 LIT 0 1000
16 STO 0 6
17 RET 0 0
""", code, "bool")

    def test_complex_bool(self):
            code = start_compiler("../sample_input/complex_bool.swift")
            self.assertEqual("""0 INT 0 3
1 LIT 0 1
2 JMC 0 26
3 LIT 0 1
4 LIT 0 -10
5 OPR 0 12
6 JMC 0 26
7 LIT 0 -5
8 LIT 0 -5
9 OPR 0 12
10 LIT 0 -1
11 OPR 0 2
12 LIT 0 -1
13 OPR 0 2
14 JMC 0 23
15 LIT 0 0
16 LIT 0 -1
17 OPR 0 2
18 JMC 0 23
19 LIT 0 0
20 LIT 0 -1
21 OPR 0 2
22 JMC 0 26
23 INT 0 1
24 LIT 0 9000
25 STO 0 3
26 RET 0 0
""", code, "complex_bool")

    def test_if_else(self):
        code = start_compiler("../sample_input/if_else.swift")
        self.assertEqual("""0 INT 0 3
1 INT 0 1
2 LIT 0 0
3 STO 0 3
4 LIT 0 52
5 LIT 0 43
6 OPR 0 10
7 JMC 0 13
8 LIT 0 32
9 LOD 0 3
10 OPR 0 4
11 STO 0 3
12 JMP 0 17
13 LIT 0 4
14 LOD 0 3
15 OPR 0 3
16 STO 0 3
17 RET 0 0
""", code, "if_else")

    def test_if_if_else(self):
        code = start_compiler("../sample_input/if_if_else.swift")
        self.assertEqual("""0 INT 0 3
1 INT 0 1
2 LIT 0 1
3 STO 0 3
4 LIT 0 52
5 LIT 0 43
6 OPR 0 10
7 JMC 0 17
8 LIT 0 100
9 LIT 0 43
10 OPR 0 10
11 JMC 0 16
12 LIT 0 32
13 LOD 0 3
14 OPR 0 4
15 STO 0 3
16 JMP 0 21
17 LIT 0 4
18 LOD 0 3
19 OPR 0 3
20 STO 0 3
21 RET 0 0
""", code, "if_if_else")

    def test_multiple_decl(self):
        code = start_compiler("../sample_input/multiple_decl.swift")
        self.assertEqual("""0 INT 0 3
1 INT 0 1
2 LIT 0 40
3 STO 0 3
4 INT 0 1
5 LOD 0 3
6 STO 0 4
7 INT 0 1
8 LOD 0 4
9 STO 0 5
10 INT 0 1
11 LOD 0 4
12 LOD 0 5
13 OPR 0 2
14 STO 0 6
15 RET 0 0
""", code, "multiple_decl")

    def test_while(self):
        code = start_compiler("../sample_input/while.swift")
        self.assertEqual("""0 INT 0 3
1 INT 0 1
2 LIT 0 5
3 STO 0 3
4 LOD 0 3
5 LIT 0 1
6 OPR 0 12
7 JMC 0 17
8 LOD 0 3
9 LIT 0 50
10 OPR 0 10
11 JMC 0 17
12 LOD 0 3
13 LIT 0 1
14 OPR 0 3
15 STO 0 3
16 JMP 0 4
17 RET 0 0
""", code, "while")

    def test_repeat_while(self):
        code = start_compiler("../sample_input/repeat.swift")
        self.assertEqual("""0 INT 0 3
1 INT 0 1
2 LIT 0 100
3 STO 0 3
4 LOD 0 3
5 LIT 0 1
6 OPR 0 3
7 STO 0 3
8 LOD 0 3
9 LIT 0 50
10 OPR 0 12
11 JMC 0 13
12 JMP 0 4
13 RET 0 0
""", code, "test_repeat_while")

    def test_for(self):
        code = start_compiler("../sample_input/for.swift")
        self.assertEqual("""0 INT 0 3
1 INT 0 1
2 LIT 0 0
3 STO 0 3
4 INT 0 1
5 LIT 0 1
6 STO 0 4
7 LOD 0 4
8 LIT 0 20
9 OPR 0 10
10 JMC 0 20
11 LIT 0 1
12 LOD 0 3
13 OPR 0 2
14 STO 0 3
15 LIT 0 1
16 LOD 0 4
17 OPR 0 2
18 STO 0 4
19 JMP 0 7
20 LIT 0 1
21 RET 0 0
""", code, "for")

    def test_func(self):
        code = start_compiler("../sample_input/func_simple.swift")
        self.assertEqual("""0 INT 0 3
1 JMP 0 28
2 INT 0 3
3 LOD 0 -3
4 LOD 0 -2
5 LOD 0 -1
6 INT 0 1
7 LIT 0 6666
8 LOD 0 3
9 OPR 0 2
10 STO 0 6
11 LOD 0 5
12 LIT 0 1000
13 OPR 0 2
14 STO 0 4
15 LIT 0 141
16 LOD 0 5
17 OPR 0 2
18 STO 0 5
19 LOD 0 6
20 LOD 0 4
21 OPR 0 2
22 LOD 0 5
23 OPR 0 2
24 STO 0 6
25 LOD 0 6
26 STO 0 -4
27 RET 0 0
28 INT 0 1
29 LIT 0 99999
30 STO 0 4
31 INT 0 1
32 INT 0 1
33 LOD 0 4
34 LIT 0 30
35 LIT 0 40
36 CAL 0 2
37 INT 0 -3
38 STO 0 5
39 RET 0 0
""", code, "func")

    def test_func_very_simple(self):
        code = start_compiler("../sample_input/func_very_simple.swift")
        self.assertEqual("""0 INT 0 3
1 INT 0 1
2 LIT 0 555
3 STO 0 3
4 INT 0 1
5 INT 0 1
6 LOD 0 3
7 CAL 0 11
8 INT 0 -1
9 STO 0 4
10 JMP 0 20
11 INT 0 3
12 LOD 0 -1
13 LIT 0 111
14 LOD 0 3
15 OPR 0 2
16 STO 0 3
17 LOD 0 3
18 STO 0 -2
19 RET 0 0
20 RET 0 0
""", code, "func_very_simple")

    def test_ternary_operator(self):
        code = start_compiler("../sample_input/ternary_operator.swift")
        self.assertEqual("""0 INT 0 3
1 INT 0 1
2 LIT 0 100
3 STO 0 3
4 LOD 0 3
5 LIT 0 43
6 OPR 0 10
7 JMC 0 12
8 LOD 0 3
9 LIT 0 9
10 OPR 0 2
11 JMP 0 15
12 LOD 0 3
13 LIT 0 5
14 OPR 0 2
15 STO 0 3
16 RET 0 0
""", code, "ternary_operator")

    def test_for_in_func(self):
            code = start_compiler("../sample_input/for_in_func.swift")
            self.assertEqual("""0 INT 0 3
1 INT 0 1
2 LIT 0 52
3 STO 0 3
4 JMP 0 27
5 INT 0 3
6 LOD 0 -1
7 INT 0 1
8 LIT 0 0
9 STO 0 4
10 LOD 0 4
11 LIT 0 1344
12 OPR 0 10
13 JMC 0 23
14 LIT 0 1
15 LOD 0 3
16 OPR 0 2
17 STO 0 3
18 LIT 0 1
19 LOD 0 4
20 OPR 0 2
21 STO 0 4
22 JMP 0 10
23 LIT 0 1
24 LOD 0 3
25 STO 0 -2
26 RET 0 0
27 INT 0 1
28 LOD 0 3
29 CAL 0 5
30 INT 0 -1
31 STO 0 3
32 RET 0 0
""", code, "for_in_func")

    def test_program(self):
        code = start_compiler("../sample_input/program.swift")
        self.assertEqual("""0 INT 0 3
1 JMP 0 27
2 INT 0 3
3 LOD 0 -1
4 INT 0 1
5 LIT 0 20
6 STO 0 4
7 LIT 0 52
8 LIT 0 43
9 OPR 0 12
10 JMC 0 21
11 INT 0 1
12 LOD 0 3
13 STO 0 5
14 LIT 0 20
15 STO 0 5
16 LIT 0 32
17 LOD 0 4
18 OPR 0 4
19 STO 0 4
20 JMP 0 25
21 LIT 0 10
22 LOD 0 4
23 OPR 0 4
24 STO 0 4
25 STO 0 -2
26 RET 0 0
27 JMP 0 49
28 INT 0 3
29 LOD 0 -1
30 INT 0 1
31 LIT 0 1
32 STO 0 4
33 LOD 0 4
34 LIT 0 21
35 OPR 0 10
36 JMC 0 46
37 LOD 0 4
38 LIT 0 5
39 OPR 0 2
40 STO 0 3
41 LIT 0 1
42 LOD 0 4
43 OPR 0 2
44 STO 0 4
45 JMP 0 33
46 LOD 0 3
47 STO 0 -2
48 RET 0 0
49 JMP 0 77
50 INT 0 3
51 LOD 0 -2
52 LOD 0 -1
53 INT 0 1
54 LIT 0 1
55 STO 0 5
56 LOD 0 5
57 LIT 0 20
58 OPR 0 10
59 JMC 0 73
60 LIT 0 1
61 LOD 0 3
62 OPR 0 2
63 STO 0 3
64 LIT 0 2
65 LOD 0 4
66 OPR 0 2
67 STO 0 4
68 LIT 0 1
69 LOD 0 5
70 OPR 0 2
71 STO 0 5
72 JMP 0 56
73 LIT 0 2
74 LOD 0 3
75 STO 0 -3
76 RET 0 0
77 JMP 0 127
78 INT 0 3
79 LOD 0 -4
80 LOD 0 -3
81 LOD 0 -2
82 LOD 0 -1
83 INT 0 1
84 LIT 0 42
85 STO 0 7
86 INT 0 1
87 LIT 0 1
88 STO 0 8
89 LOD 0 8
90 LIT 0 3
91 OPR 0 10
92 JMC 0 124
93 INT 0 1
94 LIT 0 1
95 STO 0 9
96 LOD 0 9
97 LIT 0 3
98 OPR 0 10
99 JMC 0 119
100 LOD 0 3
101 LOD 0 4
102 OPR 0 4
103 LOD 0 5
104 OPR 0 3
105 LOD 0 6
106 OPR 0 3
107 LOD 0 8
108 OPR 0 2
109 LOD 0 9
110 OPR 0 2
111 LOD 0 7
112 OPR 0 2
113 STO 0 7
114 LIT 0 1
115 LOD 0 9
116 OPR 0 2
117 STO 0 9
118 JMP 0 96
119 LIT 0 1
120 LOD 0 8
121 OPR 0 2
122 STO 0 8
123 JMP 0 89
124 LOD 0 7
125 STO 0 -5
126 RET 0 0
127 INT 0 1
128 LIT 0 0
129 STO 0 7
130 INT 0 1
131 LIT 0 0
132 STO 0 8
133 INT 0 1
134 LIT 0 43
135 CAL 0 2
136 INT 0 -1
137 STO 0 8
138 INT 0 1
139 LOD 0 7
140 LOD 0 8
141 CAL 0 50
142 INT 0 -2
143 STO 0 7
144 INT 0 1
145 LIT 0 52
146 CAL 0 2
147 INT 0 -1
148 STO 0 7
149 INT 0 1
150 LIT 0 42
151 LIT 0 42
152 LIT 0 42
153 LIT 0 42
154 CAL 0 78
155 INT 0 -4
156 STO 0 8
157 RET 0 0
""", code, "program")

    def test_complex_program(self):
        code = start_compiler("../sample_input/complex_program.swift")
        self.assertEqual("""0 INT 0 3
1 INT 0 1
2 LIT 0 52
3 STO 0 3
4 JMP 0 27
5 INT 0 3
6 LOD 0 -1
7 INT 0 1
8 LIT 0 0
9 STO 0 4
10 LOD 0 4
11 LIT 0 2
12 OPR 0 10
13 JMC 0 23
14 LIT 0 1
15 LOD 0 3
16 OPR 0 2
17 STO 0 3
18 LIT 0 1
19 LOD 0 4
20 OPR 0 2
21 STO 0 4
22 JMP 0 10
23 LIT 0 1
24 LOD 0 3
25 STO 0 -2
26 RET 0 0
27 INT 0 1
28 LOD 0 3
29 CAL 0 5
30 INT 0 -1
31 STO 0 3
32 LIT 0 100
33 LOD 0 3
34 OPR 0 10
35 JMC 0 46
36 LOD 0 3
37 LIT 0 1
38 OPR 0 3
39 STO 0 3
40 LOD 0 3
41 LIT 0 50
42 OPR 0 12
43 JMC 0 45
44 JMP 0 36
45 JMP 0 66
46 LIT 0 1
47 LOD 0 3
48 OPR 0 10
49 JMC 0 66
50 LIT 0 32
51 LOD 0 3
52 OPR 0 4
53 STO 0 3
54 LOD 0 3
55 LIT 0 43
56 OPR 0 12
57 JMC 0 62
58 LOD 0 3
59 LIT 0 9
60 OPR 0 2
61 JMP 0 65
62 LOD 0 3
63 LIT 0 5
64 OPR 0 2
65 STO 0 3
66 RET 0 0
""", code, "complex_program")

    # def test_array(self):
    #         code = start_compiler("../sample_input/not_tested/array.swift")
    #         self.assertEqual("""
    #  """, code, "array")
