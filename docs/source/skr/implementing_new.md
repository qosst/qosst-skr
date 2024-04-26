# Implementing a new SKR calculator

Implementing a new calculator might be needed to take into account more cases, or into considerations new proof. In this guide, we detail the procedure to implement a new secret key rate calculator, along with proposed guidelines.

The first step is to create a class inheriting from {external:py:class}`qosst_core.skr_computations.BaseCVQKDSKRCalculator`. This class is an abstract class with on abstract static method: {external:py:meth}`qosst_core.skr_computations.BaseCVQKDSKRCalculator.skr`. 

```{code-block} python

from qosst_core.skr_computations import BaseCVQKDSKRCalculator

class MyCalculator(BaseCVQKDSKRCalculator):
    pass
```

The goal is then to create this class and to implement the `skr` method. In order to be more flexible, the `skr` method just takes `**kwargs` as arguments. Hence one of the guideline is also to implement a `_skr` method with named arguments, while the `skr` method use `pop` to get arguments out of the `kwargs`.

```{code-block} python

from qosst_core.skr_computations import BaseCVQKDSKRCalculator

class MyCalculator(BaseCVQKDSKRCalculator):
    @staticmethod
    def skr(**kwargs) -> float:
        Va = kwargs.pop("Va")
        T = kwargs.pop("T")
        xi = kwargs.pop("xi")
        return MyCalculator._skr(Va, T, xi)

    @staticmethod
    def _skr(Va:float, T:float, xi:float) -> float:
        pass
```

From then, it's also possible other static methods to compute the different terms of the secret key rate, for instance we can implement the `_iab` and `_holevo_bound` methods:

```{code-block} python

from qosst_core.skr_computations import BaseCVQKDSKRCalculator

class MyCalculator(BaseCVQKDSKRCalculator):
    @staticmethod
    def skr(**kwargs) -> float:
        Va = kwargs.pop("Va")
        T = kwargs.pop("T")
        xi = kwargs.pop("xi")
        return MyCalculator._skr(Va, T, xi)

    @staticmethod
    def _skr(Va:float, T:float, xi:float) -> float:
        return MyCalculator._ia(Va, T, xi) - MyCalculator._holevo_bound(Va, T, xi)

    @staticmethod
    def _iab(Va:float, T:float, xi:float) -> float:
        return ...

    @staticmethod
    def _holevo_bound(Va:float, T:float, xi:float) -> float:
        return ...
```

Finally, it is needed to add some docstring, in particular to give the assumptions and a reference, and also to give the parameters in the `skr` static method:

```{code-block} python

from qosst_core.skr_computations import BaseCVQKDSKRCalculator

class MyCalculator(BaseCVQKDSKRCalculator):
    """
    This assumes:

    * this
    * and that

    References: ...

    """
    @staticmethod
    def skr(**kwargs) -> float:
        """
        This method computes the secret key rate in the case ...

        This method actually get the arguments and pass them to the _skr method that actually computes the SKR.

        Args:
            Va (float): Alice's variance of modulation (in SNU).
            T (float): transmittance of the channel.
            xi (float): excess noise of the channel (in SNU).

        Returns:
            float: secret key rate in bits per symbol.
        """
        Va = kwargs.pop("Va")
        T = kwargs.pop("T")
        xi = kwargs.pop("xi")
        return MyCalculator._skr(Va, T, xi)

    @staticmethod
    def _skr(Va:float, T:float, xi:float) -> float:
        """
        ...
        """
        return MyCalculator._ia(Va, T, xi) - MyCalculator._holevo_bound(Va, T, xi)

    @staticmethod
    def _iab(Va:float, T:float, xi:float) -> float:
        """
        ...
        """
        return ...

    @staticmethod
    def _holevo_bound(Va:float, T:float, xi:float) -> float:
        """
        ...
        """
        return ...
```