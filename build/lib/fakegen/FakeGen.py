import json
from typing import Any, List, Dict
import inspect
from anthropic import Anthropic


class FakeGen:
    """
    A class used to generate fake data based on an example object using the Anthropic API.

    Attributes
    ----------
    client : Anthropic
        The client instance for making requests to the Anthropic API.

    Methods
    -------
    generate_fake_data(example_object: Any, num_objects: int) -> List[Any]
        Generates fake data for a given example object.
    
    _infer_type(obj: Any) -> str
        Infers the type of the given object.
    
    _dict_to_object(d: Dict, obj_type: type) -> Any
        Converts a dictionary to an object of the given type.
    """

    def __init__(self, api_key: str):
        """
        Constructs all the necessary attributes for the FakeGen object.

        Parameters
        ----------
        api_key : str
            The API key for accessing the Anthropic API.
        """
        self.client = Anthropic(api_key=api_key)

    def generate_fake_data(self, example_object: Any, num_objects: int) -> List[Any]:
        """
        Generates fake data based on an example object.

        Parameters
        ----------
        example_object : Any
            The example object to base the fake data on.
        num_objects : int
            The number of fake objects to generate.

        Returns
        -------
        List[Any]
            A list of generated fake objects.

        Raises
        ------
        ValueError
            If the response from the API is not valid JSON.
        Exception
            For any other errors that occur during the API call or data processing.
        """
        try:
            # Infer the type of the example object
            inferred_type = self._infer_type(example_object)
            print(example_object)

            # Convert the example object to a JSON string
            example_json = json.dumps(
                example_object, default=lambda o: o.__dict__)

            # Prepare the prompt for Claude
            prompt = f"""Given the following example object of type {inferred_type}:
{example_json}

Please generate {num_objects} unique, diverse, and realistic fake examples of this object type. 
Ensure that the generated data maintains the same structure and data types as the example.
If the object contains any methods or complex attributes, focus on generating data for the basic attributes only.
Return the result as a valid JSON array.
Do not add any other text, just the response

"""

            # Make the API call to Claude using the Anthropic library
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=4000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # Extract the generated data from Claude's response
            text = response.content[0].text

            try:
                generated_data = json.loads(text)
            except json.JSONDecodeError:
                raise ValueError(f"Invalid JSON response: {text}")

            # Convert the generated data back to the original object type
            return [self._dict_to_object(item, type(example_object)) for item in generated_data]

        except Exception as e:
            print(f"Error occurred: {e}")
            raise

    def _infer_type(self, obj: Any) -> str:
        """
        Infers the type of the given object.

        Parameters
        ----------
        obj : Any
            The object to infer the type of.

        Returns
        -------
        str
            A string description of the object's type.
        """
        if inspect.isclass(obj):
            return f"class {obj.__name__}"
        elif isinstance(obj, dict):
            return f"dict with keys: {', '.join(obj.keys())}"
        elif isinstance(obj, list):
            if obj:
                return f"list of {self._infer_type(obj[0])}s"
            else:
                return "empty list"
        elif hasattr(obj, '__dict__'):
            return f"custom object of type {type(obj).__name__} with attributes: {', '.join(obj.__dict__.keys())}"
        else:
            return type(obj).__name__

    def _dict_to_object(self, d: Dict, obj_type: type) -> Any:
        """
        Converts a dictionary to an object of the given type.

        Parameters
        ----------
        d : Dict
            The dictionary to convert.
        obj_type : type
            The type to convert the dictionary to.

        Returns
        -------
        Any
            An object of the given type.

        Raises
        ------
        TypeError
            If the object cannot be instantiated with the given dictionary values.
        """
        try:
            if inspect.isclass(obj_type) and hasattr(obj_type, '__annotations__'):
                return obj_type(**{k: v for k, v in d.items() if k in obj_type.__annotations__})
            elif isinstance(d, dict):
                return {k: self._dict_to_object(v, type(v)) for k, v in d.items()}
            elif isinstance(d, list):
                return [self._dict_to_object(v, type(v)) for v in d]
            else:
                return d
        except TypeError as e:
            print(f"Error converting dictionary to object: {e}")
            raise
