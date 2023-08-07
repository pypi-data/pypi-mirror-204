# PyFx

The Python version of the [non-interactive, JavaScript version](https://www.npmjs.com/package/fx) of the [**fx**](https://fx.wtf). Short for *PYthon Function eXecution* or *Pyf(x)*.

```bash
python3 -mpip install pyfx
```

Or install in develop mode:

```bash
git clone https://github.com/archeraldrich/pyfx
cd pyfx
python3 setup.py develop
```

## Usage

PyFx treats arguments as Python expressions or functions. PyFx passes the input data to the first expression or function and then passes the result of the first one to the second one and so on.

```bash
echo '{"name": "world"}' | pyfx 'lambda x: x["name"]' 'lambda x: f"Hello, {x}!"'
```

Use `self` to access the input data. Use `.` at the start of the expression to access the input data without a `lambda x: x` part.

```python
echo '{"name": "world"}' | pyfx '.get("name")' 'f"Hello, {self}!"'
```

Use other Python functions to process the data.

```python
echo '{"name": "world"}' | pyfx 'dict.keys' 'list'
```

## Advanced Usage

PyFx can process a stream of JSON objects. PyFx will apply arguments to each object.

```bash
printf '{"name": "hello"}\n{"name": "world"}' | pyfx '.get("name")'
```

If you want to process a stream of JSON objects as a single list, use the **--slurp** or **-s** flag.

```python
printf '{"name": "hello"}\n{"name": "world"}' | pyfx --slurp 'list(map(lambda x: x.get("name"), self))' '", ".join'
```

If you want to process non-JSON data, use the **--raw** or **-r** flag.

```bash
ls | pyfx -r '[self, self.find(".md") != -1]'
```

You can use **--raw** and **--slurp** (or **-rs**) together to get a single array of strings.

```bash
ls | pyfx -rs 'list(filter(lambda x: x.find(".md") != -1, self))'
```

PyFx has a special symbol `skip` for skipping the printing of the result.

```bash
ls | pyfx -r 'self if self.find(".md") != -1 else skip'
```

PyFx comes with the import statement. Use the **--import** or **-i** command once per import statement, without the leading `import` keyword. 

```bash
seq 1 100 | pyfx -rs -i 'numpy as np' -i 'from matplotlib import pyplot as plt' 'list(map(int, self))' 'np.array' 'plt.plot' 'lambda _: plt.show()'
```

## License

[MIT](LICENSE)
