# HugChat - AI in your Terminal

Use [HuggingChat](https://huggingface.co/chat) without leaving your terminal, just copy the `ai.py` file to wherever you want and you are good to go. (ofcourse you need Python with Pip)

It just has 2 dependencies that can be installed from the command

```
pip install requests inquirer
```

For linux devices, you just need to change the permission by using the command

```
chmod 777 ai.py
```

To run, use the command

```
./ai.py
```

While it's possible to use this feature without creating an account, you can enhance your experience by utilizing the `config.json` file to incorporate cookies from your [HuggingFace](https://huggingface.co/) account. Doing so can reduce errors and improve overall performance. If you're unfamiliar with how to use cookies, don't worry - it's not a requirement. However, if you are familiar with this process, you don't need to set all fields. Please note that using the config file solely to set null values is not recommended.
