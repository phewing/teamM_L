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

        self.assertEqual(
            parse_relationship_text("mate mother"),
            StepSequence([Step(StepDirection.MATE), Step(StepDirection.MOTHER)])
        )

        self.assertEqual(
            parse_relationship_text("sibling twin"),
            StepSequence([Step(StepDirection.SIBLING)])
        )

        self.assertEqual(
            parse_relationship_text("sibling 2"),
            StepSequence([Step(StepDirection.SIBLING)])
        )


