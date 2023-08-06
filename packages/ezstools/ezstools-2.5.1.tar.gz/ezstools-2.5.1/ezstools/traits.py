"""
Provides the ability to define, implement and specify traits for classes. Just link Rust's traits. 
"""
from typing import Callable, Self, Set, Type, TypeVar, Generic, Union

# Typing hints for traits
T = TypeVar("T", bound=object)

class impls(Generic[T]):
    """
    Typing hint for traits.
    Example:
    ```python
    def foo(bar: Impls[MyTrait]):
        pass
    ```
    """

    def __init__(self, *traits):
        self.traits = traits

    def __repr__(self):
        return f"Traits[{', '.join(t.__name__ for t in self.traits)}]"

    def __getitem__(self, item):
        return self.traits[item]

class TraitType(type):
    """
    Base class for traits.
    """

    NotImplementedError = NotImplementedError("You must implement this method")

    def __init__(self, trait_methods: Set[str]) -> None:
        self._implemented_traits: Set[str] = set()
        self._trait_methods: Set[str] = trait_methods
        self._verify_trait_methods = TraitType._verify_trait_methods


    @staticmethod
    def _verify_trait_methods(trait: Type[Self], instance: type) -> None:
        """
        Verifies that all trait methods have been implemented.
        """
        if trait._trait_methods != trait._implemented_traits:
            raise NotImplementedError(
                f"Class {instance.__class__.__name__} does not implement all trait methods of trait {trait.__name__}. Missing methods: {trait._trait_methods - trait._implemented_traits}"
            )


def setup_traits(instance: type, traits: Set[TraitType]):
    """
    Sets up the trait's for a class.
    """
    instance._traits: Set[TraitType] = traits
    cls = instance.__class__

    cls_methods = [
        name
        for name, func in vars(cls).items()
        if not name.startswith("_") and callable(func)
    ]

    # Initialize the traits
    for trait in instance._traits:
        trait.__init__(trait)

    # Get the methods of the class and add them to the trait's implemented methods
    for method_name in cls_methods:
        for trait in instance._traits:
            if method_name in trait._trait_methods:
                trait._implemented_traits.add(method_name)
                break

    # Verify that all trait methods have been implemented
    for trait in instance._traits:
        trait._verify_trait_methods(trait, instance)

def create_trait(trait_cls: type):
    """
    Creates a trait from a class. This is done by creating a new class that inherits from the class passed as an argument.
    """

    def __init__(self: TraitType):
        TraitType.__init__(self, 
            set(
                [
                    name
                    for name, func in trait_cls.__dict__.items()
                    if not name.startswith("_") and callable(func)
                ]
            ),
        )

    trait_cls.__init__ = __init__
    instance = trait_cls()

    return instance

def trait(cls: type) -> type:
    """
    #### Creates a trait from a class.
    #### Example:
    ```python
    @trait
    class MyTrait:
        def trait_method(self):
            ...
    ```
    Manually creating a trait:
    ```python
    class MyTrait(TraitType): # Inherit from TraitType is optional
        def trait_method(self):
            ...

    MyTrait = create_trait(MyTrait)
    ```
    """
    create_trait(cls)
    return cls

def implements(*traits: TraitType):
    """
    #### Sets up the traits for a class.
    #### Parameters:
    - `traits`: The traits to implement.

    #### Example:
    ```python
    @implements(MyTrait)
    class MyClass:
        ...
        def trait_method(self):
            ...
    ```
    """

    def decorate_cls(cls: type):
        # save the original __init__ method
        cls_init = cls.__init__

        # setup traits after __init__ has been called
        def __init__(self, *args, **kwargs):
            cls_init(self, *args, **kwargs)
            setup_traits(self, traits)

        cls.__init__ = __init__

        return cls

    return decorate_cls

def verify_traits(func: Callable) -> Callable:
    """
    #### Verifies that the Parameter of a function has the annotated traits.
    #### Example:
    ```python
    @verify_traits
    def foo(bar:impls[MyTrait]): # Bar must have the trait MyTrait otherwise a TypeError will be raised
        ...
    ```
    """

    def wrapper(*args, **kwargs):

        # Get the function's annotations
        annotations = func.__annotations__

        # Check if the function has any annotations
        if not annotations:
            raise TypeError(
                f"Function {func.__name__} does not have any annotations. Try adding: `Impls[YourTraitType]` as a annotation to the parameter that needs to be verified."
            )

        # iterate over the annotations
        for name, annotation in annotations.items():
            if not getattr(annotation, "__origin__", None):
                continue

            # Check if the annotation is a Traits type
            if not annotation.__origin__ == impls:
                continue

            # Get the parameter from the function's arguments
            parameter = dict(zip(func.__code__.co_varnames, args)).get(name, None) or kwargs.get(name, None)
                
            required_traits = set(annotation.__args__)
            parameter_traits = getattr(parameter, "_traits", set())

            # Check if the parameter has the required traits
            if not parameter_traits or not set(required_traits).issubset(
                parameter._traits
            ):
                missing_traits = set(map(lambda o: o.__name__, set(required_traits) - parameter_traits))

                raise TypeError(
                    f"`{name}` (parameter at {func.__name__}) does not have all required traits. Missing traits: {missing_traits}"
                )

        return func(*args, **kwargs)

    return wrapper
