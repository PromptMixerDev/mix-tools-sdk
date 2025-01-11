Usage Guide
===========

This guide will help you get started with using the Mix Tools SDK.

Basic Usage
----------

First, import and initialize the client:

.. code-block:: python

    from mix_tools_sdk import Client

    client = Client("your-api-key")

Making API Requests
----------------

The client provides methods for interacting with the Mix Tools API:

.. code-block:: python

    # Example API request
    response = await client.some_method()

Error Handling
------------

The SDK uses custom exceptions to handle various error cases:

.. code-block:: python

    from mix_tools_sdk import Client, APIError

    try:
        client = Client("your-api-key")
        response = await client.some_method()
    except APIError as e:
        print(f"API Error: {e}")

Configuration
-----------

You can configure the client with additional options:

.. code-block:: python

    client = Client(
        api_key="your-api-key",
        base_url="https://api.example.com",  # Optional
        timeout=30  # Optional
    )

Advanced Usage
------------

For more complex scenarios, the SDK provides additional functionality:

.. code-block:: python

    # Example of advanced usage
    async with Client("your-api-key") as client:
        # Client will automatically close after the block
        response = await client.some_method()

Best Practices
------------

1. Always use async/await when making API calls
2. Handle potential exceptions appropriately
3. Use context managers when possible
4. Keep your API key secure
5. Set appropriate timeouts for your use case
