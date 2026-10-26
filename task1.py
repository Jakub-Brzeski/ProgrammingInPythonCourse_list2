import unittest


class Solution:
    """Represents a solution of a given substance.

        Attributes:
            name (str): Name of the solute.
            concentration (int or float): Concentration of the solution in mg/mL.
            volume (int or float): Total volume of the solution in mL.
    """
    def __init__(self, name, concentration, volume):
        """Initializes a Solution object after validating inputs.

        Args:
            name (str): Name of the solute.
            concentration (int or float): Concentration in mg/mL (must be > 0).
            volume (int or float): Volume in mL (must be > 0).

        Raises:
            TypeError: If arguments are of incorrect types.
            ValueError: If concentration or volume is <= 0.
        """

        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        if not isinstance(concentration, (float, int)) or isinstance(concentration, bool):
            raise TypeError("Concentration must be a number")
        if not isinstance(volume, (float, int)) or isinstance(volume, bool):
            raise TypeError("Volume must be a number")
        if concentration<=0:
            raise ValueError("Concentration must be bigger than 0")
        if volume<=0:
            raise ValueError("Volume must be bigger than 0")

        self.name = name
        self.concentration = concentration
        self.volume = volume


    def __str__(self):
        """Returns formatted string representation of the solution."""
        return (f"Solution: {self.name}\n"
                f"Concentration: {round(self.concentration, 2)} mg/mL\n"
                f"Volume: {round(self.volume, 2)} mL")

    def add(self, other):
        """Combines two solutions of the same solute, updating concentration and volume.

        Args:
            other (Solution): Another Solution object to mix in.

        Raises:
            TypeError: If other is not a Solution instance.
            ValueError: If the solutes have different names.
        """

        if not isinstance(other, Solution):
            raise TypeError("Selected object must be a solution")
        if self.name != other.name:
            raise ValueError("Can't combine these solutions, because they aren't of the same solute")

        mass1: float = float(self.concentration*self.volume)
        mass2: float = float(other.concentration*other.volume)
        self.volume = self.volume + other.volume
        self.concentration = (mass1 + mass2)/self.volume
        other.concentration = 0
        other.volume = 0

    def dilute(self, factor):
        """Reduces the solution concentration by a given dilution factor.

        Args:
            factor (int or float): Dilution factor (must be > 1).

        Raises:
            TypeError: If factor is not a number.
            ValueError: If factor <= 1.
        """
        if not isinstance(factor, (float, int)) or isinstance(factor, bool):
            raise TypeError("Factor must be a number")
        if factor <= 1:
            raise ValueError("Factor must be bigger than 1 to dilute the solution")
        self.concentration = self.concentration / factor
        self.volume = self.volume * factor

    def __eq__(self, other):
        """Returns True if two solutions have the same name and concentration."""
        if not isinstance(other, Solution):
            return False
        return self.name == other.name and self.concentration == other.concentration

class TestSolution(unittest.TestCase):
    """Unit tests for the Solution class."""

    def test_typical_values(self):
        s1 = Solution("NaCl", 10.0, 100.0)
        s2 = Solution("NaCl", 20.0, 100.0)

        self.assertIn("NaCl", str(s1))

        s1.add(s2)
        self.assertEqual(s1.concentration, 15.0)
        self.assertEqual(s1.volume, 200.0)
        self.assertEqual(s2.concentration, 0.0)
        self.assertEqual(s2.volume, 0.0)

        s1.dilute(2)
        self.assertEqual(s1.concentration, 7.5)
        self.assertEqual(s1.volume, 400.0)

        s3 = Solution("NaCl", 7.5, 50.0)
        self.assertEqual(s1, s3)

    def test_boundary_values(self):
        s1 = Solution("NaCl", 0.001, 0.001)
        self.assertEqual(s1.concentration, 0.001)

        s1.dilute(1.0001)
        self.assertGreater(s1.volume, 0.001)

    def test_exceptions(self):
        with self.assertRaises(TypeError):
            Solution(123, 10, 100)
        with self.assertRaises(TypeError):
            Solution("NaCl", "ten", 100)
        with self.assertRaises(TypeError):
            Solution("NaCl", True, 100)
        with self.assertRaises(ValueError):
            Solution("NaCl", -5, 100)
        with self.assertRaises(ValueError):
            Solution("NaCl", 10, 0)

        s1 = Solution("NaCl", 10, 100)
        s2 = Solution("notNaCl", 10, 100)
        with self.assertRaises(ValueError):
            s1.add(s2)
        with self.assertRaises(TypeError):
            s1.add("not a solution")

        with self.assertRaises(ValueError):
            s1.dilute(1)
        with self.assertRaises(ValueError):
            s1.dilute(0.5)
        with self.assertRaises(TypeError):
            s1.dilute("two")


if __name__ == '__main__':
    unittest.main()