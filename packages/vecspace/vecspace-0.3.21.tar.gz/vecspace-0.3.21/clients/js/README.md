## vecspace

VecSpace is the open-source embedding database. VecSpace makes it easy to build LLM apps by making knowledge, facts, and skills pluggable for LLMs.

This package gives you a JS/TS interface to talk to a backend VecSpace DB over REST. 

[Learn more about VecSpace](https://github.com/vecspace-core/vecspace)

- [💬 Community Discord](https://discord.gg/MMeYNTmh3x)
- [📖 Documentation](https://docs.tryvecspace.com/)
- [💡 Colab Example](https://colab.research.google.com/drive/1QEzFyqnoFxq7LUGyP1vzR4iLt9PpCDXv?usp=sharing)
- [🏠 Homepage](https://www.tryvecspace.com/)

## Getting started

VecSpace needs to be running in order for this client to talk to it. Please see the [🧪 Usage Guide](https://docs.tryvecspace.com/usage-guide) to learn how to quickly stand this up. 

## Small example


```js
import { VecSpaceClient } from "vecspace"
const vecspace = new VecSpaceClient("http://localhost:8000");
const collection = await vecspace.createCollection("test-from-js");
for (let i = 0; i < 20; i++) {
    await collection.add(
      "test-id-" + i.toString(),
      [1, 2, 3, 4, 5],
      { "test": "test" }
    )
}
const queryData = await collection.query([1, 2, 3, 4, 5], 5, { "test": "test" });
```

## Local development

[View the Development Readme](./DEVELOP.md)

## License

Apache 2.0