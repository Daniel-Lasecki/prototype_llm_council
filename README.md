# Prototype LLM Council
This was just a test of multiple ai models running on my personal pc

Leader.Modelfile is just an example for other council members modelfiles
```bash
ollama list
NAME                      ID              SIZE     
llama2-uncensored:7b      44040b922233    3.8 GB    
mistral:latest            6577803aa9a0    4.4 GB       
nous-hermes2:latest       d50977d0b36a    6.1 GB     
mixtral:latest            a3b6bef0f836    26 GB        
dolphin-mistral:latest    5dc8c5a2be65    4.1 GB    
```
specs:

Nvidia 40-series gpu 12gb vram 

Amd am5 8-cores

32gb ram

---------------------------------------------

For memory i tried using .json with ai derived [tags] of the topic.
Adding memory works but fetching and tags are a mess. 
```json
{
  "entries": [
    {
      "topic": "506523452443786719c900478af6fd7c",
      "summary": "To make strawberrycake, combine strawberries, sugar, cornstarch, and butter in a saucepan and cook over medium heat until the mixture thickens. Add the remaining ingredients and stir to combine. Pour into a greased baking dish and bake for about 30 minutes.",
      "tags": [
        "- astronomy",
        "- projects",
        "- cooking",
        "- work",
        "- school"
      ]
    }
  ]
```

Conclusion: rotting prototype project to rot on my github page
