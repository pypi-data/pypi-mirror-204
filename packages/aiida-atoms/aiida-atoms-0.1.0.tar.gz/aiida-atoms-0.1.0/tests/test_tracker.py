"""
Test the tracker
"""

from ase.build import bulk
import numpy as np
import pytest

from aiida import orm

from aiida_atoms.tracker import AtomsTracker


def check_atoms_equality(a1, a2, tol=1e-10):
    """Check if two atoms are equivalent"""
    if isinstance(a1, AtomsTracker):
        a1 = a1.atoms
    if isinstance(a2, AtomsTracker):
        a2 = a2.atoms

    assert abs(a1.cell - a2.cell).max() < tol
    assert abs(a1.positions - a2.positions).max() < tol
    assert abs(a1.numbers == a2.numbers).all()


def check_atoms_inequality(a1, a2, tol=1e-10):
    """Check if two atoms are inequivalent"""
    if isinstance(a1, AtomsTracker):
        a1 = a1.atoms
    if isinstance(a2, AtomsTracker):
        a2 = a2.atoms

    assert any(
        [
            (abs(a1.cell - a2.cell).min() > tol),
            (abs(a1.positions - a2.positions).min() > tol),
            abs(a1.numbers != a2.numbers).any(),
        ]
    )


mgo = bulk("MgO", "rocksalt", 4.0)


@pytest.mark.parametrize(
    ["inplace", "atoms", "method_name", "args", "kwargs"],
    [
        [True, mgo, "translate", [(0.1, 0.1, 0.1)], {}],
        [True, mgo, "center", [], {}],
        [True, mgo, "wrap", [], {}],
        [True, mgo, "rattle", [0.1], {}],
        [True, mgo, "rattle", [], {"stdev": 0.1}],
        [True, mgo, "set_cell", [np.diag([3, 3, 3])], {}],
        [True, mgo, "set_cell", [np.diag([3, 3, 3])], {"scale_atoms": True}],
        [True, mgo, "set_atomic_numbers", [[1, 1]], {}],
        [True, mgo, "set_masses", [[1, 1]], {}],
        [True, mgo, "set_distance", [0, 1], {"distance": 1.0}],
        [False, mgo, "__mul__", [(2, 2, 2)], {}],
        [False, mgo, "repeat", [(2, 2, 2)], {}],
        [False, mgo, "__getitem__", [[0]], {}],
    ],
)
def test_track_roundtrip(inplace, atoms, method_name, args, kwargs):
    """
    Perform tests for using the tracker to track in-place and out-of-place operations.
    Test round trip equality of the results.
    """
    init_state = atoms.copy()
    tracker = AtomsTracker(atoms)

    # Apply the operation
    returned_obj = getattr(tracker, method_name)(*args, **kwargs)
    if inplace:
        oped_atoms = atoms
        # Operate on the intitial state
        atoms_returned_obj = getattr(init_state, method_name)(*args, **kwargs)
        assert returned_obj == atoms_returned_obj
    else:
        oped_atoms = getattr(atoms, method_name)(*args, **kwargs)
        check_atoms_equality(atoms, init_state)
        check_atoms_equality(oped_atoms, returned_obj)


def test_tracker_wrap_node():
    """Test if a tracker can wrap methods of the node correctly"""
    tracker1 = AtomsTracker(mgo)
    assert tracker1.label == ""

    tracker1.label = "Node1"
    assert tracker1.label == "Node1"
    assert tracker1.node.label == "Node1"

    tracker1.description = "Node1"
    assert tracker1.description == "Node1"
    assert tracker1.node.description == "Node1"

    tracker1.store_node()
    tracker1.base.extras.set("a", 1)
    assert tracker1.base.extras.get("a") == 1


def test_tracker_construction():
    """Test `AtomsTracker` type"""

    tracker1 = AtomsTracker(mgo)
    mgo_node = orm.StructureData(ase=mgo)
    tracker2 = AtomsTracker(mgo_node)

    check_atoms_equality(tracker1, tracker2)

    assert tracker1.node.is_stored is False
    assert tracker2.node.is_stored is False

    tracker1.repeat((2, 2, 2))
    assert tracker1.node.is_stored


def test_provenance_tracking(clear_database):
    """Test if the provenance graph created is correct"""

    # Perform a mixture of inplace and out-of-place operations with branching
    tracker = AtomsTracker(mgo)
    node_init = tracker.node
    _ = tracker.repeat((3, 3, 3))
    tracker = tracker.repeat((2, 2, 2))
    node_1 = tracker.node
    tracker.pop(0)
    node_2 = tracker.node
    tracker.pop(0)
    node_3 = tracker.node

    assert node_init.is_stored
    assert node_2.is_stored

    assert len(node_init.get_outgoing().all()) == 2
    assert len(node_1.get_outgoing().all()) == 1
    assert len(node_2.get_outgoing().all()) == 1
    assert len(node_1.get_incoming().one().node.get_incoming().all()) == 2
    assert len(node_2.get_incoming().one().node.get_incoming().all()) == 2
    assert len(node_3.get_incoming().one().node.get_incoming().all()) == 2
