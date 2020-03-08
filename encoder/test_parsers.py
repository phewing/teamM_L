from unittest import TestCase

from parsers import parse_relationship_text, StepSequence, StepDirection, Step


class TestParsers(TestCase):
    def test_parse_relationship_text(self):
        self.assertEqual(
            parse_relationship_text("self"),
            StepSequence()
        )

        self.assertEqual(
            parse_relationship_text("mate"),
            StepSequence([Step(StepDirection.MATE)])
        )

        a = parse_relationship_text("mate mother")
        b = StepSequence([Step(StepDirection.MATE), Step(StepDirection.MOTHER)])

        self.assertEqual(
            a, b
        )

        self.assertEqual(
            parse_relationship_text("sibling twin"),
            StepSequence([Step(StepDirection.SIBLING)])
        )

        a = parse_relationship_text("sibling 2")
        b = StepSequence([Step(StepDirection.SIBLING, 2)])

        self.assertEqual(
            a, b
        )

        self.assertEqual(
            parse_relationship_text("paternal grandmother"),
            StepSequence([Step(StepDirection.FATHER), Step(StepDirection.MOTHER)])
        )

        self.assertEqual(
            parse_relationship_text("paternal grandfather sibling 1 child mate"),
            StepSequence([Step(StepDirection.FATHER),
                          Step(StepDirection.FATHER),
                          Step(StepDirection.SIBLING, 1),
                          Step(StepDirection.CHILD),
                          Step(StepDirection.MATE)
                          ])
        )

        self.assertEqual(
            parse_relationship_text("paternal grandfather sibling 1 child mate identical twin"),
            StepSequence([Step(StepDirection.FATHER),
                          Step(StepDirection.FATHER),
                          Step(StepDirection.SIBLING, 1),
                          Step(StepDirection.CHILD),
                          Step(StepDirection.MATE)
                          ])
        )

        a = parse_relationship_text("paternal grandfather sibling 1 child 3 father identical twin mate 2 mother child")
        b = StepSequence([Step(StepDirection.FATHER),
                          Step(StepDirection.FATHER),
                          Step(StepDirection.SIBLING, 1),
                          Step(StepDirection.CHILD, 3),
                          Step(StepDirection.FATHER),
                          Step(StepDirection.MATE, 2),
                          Step(StepDirection.MOTHER),
                          Step(StepDirection.CHILD)
                          ])

        self.assertEqual(
            a, b
        )
