# BatchTx
The JSON-RPC specification outlines how clients can send multiple requests at the same time by filling the request objects in an array. This feature is implemented by Geth's API and can be used to cut network delays. Batching offers visible speed-ups specially when used for fetching larger amounts of mostly independent data objects.
