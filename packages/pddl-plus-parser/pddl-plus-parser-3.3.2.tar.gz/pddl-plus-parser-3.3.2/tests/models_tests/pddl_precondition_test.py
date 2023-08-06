"""Module that tests the functionality of the pddl_precondition module."""
from pddl_plus_parser.lisp_parsers import DomainParser
from pddl_plus_parser.models import Predicate, Domain
from pddl_plus_parser.models.pddl_precondition import CompoundPrecondition, Precondition

from pytest import fixture, fail

from tests.models_tests.consts import TEST_HARD_NUMERIC_DOMAIN


@fixture()
def domain() -> Domain:
    domain_parser = DomainParser(TEST_HARD_NUMERIC_DOMAIN)
    return domain_parser.parse_domain()


@fixture()
def simple_precondition() -> Precondition:
    return Precondition("and")


def test_add_condition_adds_a_single_predicate_correctly(simple_precondition: Precondition, domain: Domain):
    test_predicate = domain.predicates["on_board"]
    simple_precondition.add_condition(test_predicate)
    assert str(simple_precondition) == "(and (on_board ?i ?s))"


def test_add_condition_when_given_the_same_predicate_twice_does_not_add_it_a_second_time(
        simple_precondition: Precondition, domain: Domain):
    test_predicate = domain.predicates["on_board"]
    simple_precondition.add_condition(test_predicate)
    simple_precondition.add_condition(test_predicate)
    assert str(simple_precondition) == "(and (on_board ?i ?s))"


def test_add_condition_with_nested_preconditions_keeps_both_copies_of_the_predicates(
        simple_precondition: Precondition, domain: Domain):
    test_predicate1 = domain.predicates["on_board"]
    test_predicate2 = domain.predicates["supports"]
    negative_predicate = test_predicate1.copy()
    negative_predicate.is_positive = False

    nested_condition = Precondition("or")
    nested_condition.add_condition(negative_predicate)
    nested_condition.add_condition(test_predicate2)
    simple_precondition.add_condition(test_predicate2)
    simple_precondition.add_condition(nested_condition)

    assert str(simple_precondition).count("(supports ?i ?m)") == 2
    assert str(simple_precondition).count("(on_board ?i ?s)") == 1
