# CrowdCores Pipeline 

Learn more about [CrowdCores on the official website](https://www.crowdcores.com)

To run a CrowdCores Pipeline install the package:

```
pip3 install crowdcores
```

The crowdcores_pipeline works just the same as transformers pipeline from hugging face, you simply need to import crowdcores_pipeline and replace any pipeline calls with crowdcores_pipeline. Here is an example:


```
from crowdcores import crowdcores_pipeline
#from transformers import pipeline
...
...


#note: we use crowdcore_pipeline instead of pipeline
#generator=pipeline('text-generation', model='gpt2');
generator=crowdcores_pipeline('text-generation', model='gpt2');
r=generator("how are you doing ", max_length=30, num_return_sequences=4)
print(r)
```

