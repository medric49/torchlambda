<img align="left" width="256" height="256" src="https://github.com/szymonmaszke/torchlambda/blob/master/assets/banner.png">

[__torchlambda__](https://szymonmaszke.github.io/torchlambda/) is a tool to deploy [PyTorch](https://pytorch.org/) models
on [Amazon's AWS Lambda](https://aws.amazon.com/lambda/) using [AWS SDK for C++](https://aws.amazon.com/sdk-for-cpp/)
and [custom C++ runtime](https://github.com/awslabs/aws-lambda-cpp).

Using statically compiled dependencies __whole package is shrunk to only `30MB`__.

Due to small size of compiled source code users can pass their models as [AWS Lambda layers](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html).
__Services like [Amazon S3](https://aws.amazon.com/s3/) are no longer needed to load your model__.

[__torchlambda__](https://szymonmaszke.github.io/torchlambda/) has it's PyTorch & AWS dependencies always up to date because of [continuous deployment](https://en.wikipedia.org/wiki/Continuous_deployment) run at `03:00 a.m.`
every day.


| Docs | Status | Package | Python | PyTorch | Docker | CodeBeat | Images |
|------|--------|---------|--------|---------|--------|----------|--------|
|[![Documentation](https://img.shields.io/static/v1?label=&message=Wiki&color=EE4C2C&style=for-the-badge)](https://github.com/szymonmaszke/torchlambda/wiki) | ![CD](https://img.shields.io/github/workflow/status/szymonmaszke/torchlambda/tests?label=%20&style=for-the-badge) | [![PyPI](https://img.shields.io/static/v1?label=&message=PyPI&color=377EF0&style=for-the-badge)](https://pypi.org/project/torchlambda/) | [![Python](https://img.shields.io/static/v1?label=&message=>=3.6&color=377EF0&style=for-the-badge&logo=python&logoColor=F8C63D)](https://www.python.org/) | [![PyTorch](https://img.shields.io/static/v1?label=&message=>=1.4.0&color=EE4C2C&style=for-the-badge)](https://pytorch.org/) | [![Docker](https://img.shields.io/static/v1?label=&message=>17.05&color=309cef&style=for-the-badge)](https://cloud.docker.com/u/szymonmaszke/repository/docker/szymonmaszke/torchlambda) | [![codebeat badge](https://codebeat.co/badges/ca6f19c8-29ad-4ddb-beb3-4d4e2fb3aba2)](https://codebeat.co/projects/github-com-szymonmaszke-torchlambda-master) | [![Images](https://img.shields.io/static/v1?label=&message=Tags&color=309cef&style=for-the-badge)](https://hub.docker.com/r/szymonmaszke/torchlambda/tags)|


This README provides only basic introduction, for full picture
[please see documentation](https://github.com/szymonmaszke/torchlambda/wiki)
and command line `--help` flag.

# Comparison with other deployment tools

__Improve this comparison's reliability via [Pull Request](https://github.com/szymonmaszke/torchlambda/pulls?q=is%3Apr+is%3Aopen+sort%3Aupdated-desc), thanks.
Also show guys below some love by visiting their projects (just click on the name).__

Trait / Tool | torchlambda | [fastai Lambda](https://course.fast.ai/deployment_aws_lambda.html) | [KubeFlow](https://www.kubeflow.org/) | [Tensorflow Serving](https://github.com/tensorflow/serving) |
|------------|-------------|--------------------------------------------------------------------|------------------|--------------------|
__Autoscaling__ |:heavy_check_mark: | :heavy_check_mark: | with [Kubernetes](https://kubernetes.io/) | with [Kubernetes](https://kubernetes.io/) |
__Light/Heavy load__ | Light  | Light | Heavy/Both | Both |
__GPU Support__ | :x: | :x: | :heavy_check_mark: | :heavy_check_mark: |
__Serverless__ |:heavy_check_mark: | :heavy_check_mark: | :x: | :x: |
__Required services__ | AWS Lambda | AWS Lambda, AWS S3 | Kubernetes Cluster & cloud provider | Deployable in various settings |
__Multiple frameworks__ | :x:  | :x: | :heavy_check_mark: | :x: |
__Latest framework__ <sup>[1](#footnote1)</sup> | :heavy_check_mark: | :x: | :x: | :heavy_check_mark: |
__Version (higher more mature)__ | [CD](https://en.wikipedia.org/wiki/Continuous_deployment) | N/A | [1.0](https://github.com/kubeflow/kubeflow/releases/tag/v1.0) | [2.1.0](https://github.com/tensorflow/serving/releases/tag/2.1.0) |
__Customizable dependencies__ <sup>[2](#footnote2)</sup> | :heavy_check_mark: | :x: | :x: | :x: |
__Deployment size__ <sup>[3](#footnote3)</sup>| ~30Mb| +1Gb | N/A | ~67Mb<sup>[4](#footnote4)</sup> |



# Installation

- [Docker](https://docs.docker.com/) at least of version `17.05` is required.
See [Official Docker's documentation](https://docs.docker.com/) for installation
instruction specific to your operating system

- Install `torchlambda` through [pip](https://pypi.org/project/pip/), [Python](https://www.python.org/)
version `3.6` or higher is needed. You could also install this software within [conda](https://docs.conda.io/en/latest/)
or other virtual environment of your choice. Following command should be sufficient:

  ```shell
  $ pip install --user torchlambda
  ```

__torchlambda provides pre-built deployment images tagged after PyTorch versions and rebuilt daily.__ Following images are currently available:

- [`szymonmaszke/torchlambda:latest`](https://hub.docker.com/layers/szymonmaszke/torchlambda/latest/images/sha256-7d493f3b61d37446466e3140ba516bd18179781a05cfe0331bf833f551a37f0e?context=explore) (head of current PyTorch master branch)
- [`szymonmaszke/torchlambda:1.4.0`](https://hub.docker.com/layers/szymonmaszke/torchlambda/v1.4.0/images/sha256-e92361e5fc1ecc91200d63a1d4d0c88c3f91cd7aff3859689f1542cec4956a43?context=explore)

For more info refer to [`torchlambda build` documentation](https://github.com/szymonmaszke/torchlambda/wiki/Commands#torchlambda-build)
and how to build your own custom images to use for deployment.

# Example deploy

Below is a mini-tutorial on deployment of [ResNet18](https://arxiv.org/abs/1512.03385) image classifier using `torchlambda`.
__This is only an example__, for more sophisticated use cases (e.g. `base64` encoding of image or testing deployment locally)
see [Tutorials](https://github.com/szymonmaszke/torchlambda/wiki/Tutorials) section.

## 1. Create model to deploy

Below is a code (`model.py`) to load `ResNet` from [`torchvision`](https://pytorch.org/docs/stable/torchvision/models.html#classification)
and compile is to [`torchscript`](https://pytorch.org/tutorials/beginner/Intro_to_TorchScript_tutorial.html):

```python
import torch
import torchvision

model = torchvision.models.resnet18()

# Smaller example
example = torch.randn(1, 3, 64, 64)
script_model = torch.jit.trace(model, example)

script_model.save("model.ptc")
```

Invoke it from CLI:

```
$ python model.py
```

You should get `model.ptc` in your current working directory.

## 2. Create settings

`torchlambda` uses C++ to deploy models hence it might be harder for end users
to provide necessary source code.

To alleviate some of those issues easy to understand `YAML` settings can be used
to define `outputs` and various elements of neural network and deployment.

Please run the following:

```shell
torchlambda settings
```

This command will generate `torchlambda.yaml` file with __all available commands__
for you to modify according to your needs. You can see all of them
with short description below.

<details>

  __<summary> Click here to check generated YAML settings </summary>__

```yaml
---
grad: False # Turn gradient on/off
validate_json: true # Validate correctnes of JSON parsing
model: /opt/model.ptc # Path to model to load
input: # Define properties of input
  name: data # Name of field containing data
  validate_field: true # Whether above field will be checked for correctness
  type: float # Type of data in this field (array assumed or base64)
  shape: [1, 3, width, height] # Input shapes (int or name of field as str)
  validate_shape: true # Whether to validate fields containing shape info
cast: float # Type to which tensor will be casted before inference (if any)
divide: 255 # Value by which it will be divided (if any)
normalize: # Whether to normalize the tensor
  means: [0.485, 0.456, 0.406] # Using those means
  stddevs: [0.229, 0.224, 0.225] # And those standard deviations
return: # Finally return something in JSON
  output: # Unmodified output from neural network
    type: double # Casted to double type (AWS SDK compatible)
    name: output # Name of the field where value(s) will be returned
    item: false # If we return single value use True, neural network usually returns more (an array)
  result: # Return another field result by modifying output
    operations: argmax # Apply argmax (more operations can be specified as list)
    arguments: 1 # Over first dimension (more or no arguments can be specified)
    type: int # Type returned will be integer
    name: result # Named result
    item: true # It will be a single item
```

</details>
&nbsp;


Many fields already have sensible defaults ([see YAML settings file reference](https://github.com/szymonmaszke/torchlambda/wiki/YAML-settings-file-reference))
hence they will be left for now.
In our case we will only define bare minimum:

```yaml
---
input:
  shape: [1, channels, width, height]
  type: byte
cast: float
divide: 255
return:
  result:
    operations: argmax
    type: int
    name: label
    item: true
```

- `input` -  tensor of shape `[1, channels, width, height]`, where batch size always equal to `1`
(static), variable number of channels and variable width and height could be used. Last three
elements should be passed as `int` fields in JSON request and named accordingly (
`channels`, `width` and `height`).
`type` of tensor is specified as `byte` (image with values in range `[0, 255]`).
- Created tensor will be `cast`ed to `float`
- And `divide`d by `255` to be in `[0,1]` range as `ResNet18` expects.
- `return` - return output of the network modified by `argmax`
operation which creates `result`.
Our returned `type` will be `int`, and JSON field `name` (__`torchlambda` always returns JSONs__)
will be `label`. `argmax` over `tensor` will create single (by default the operation is applied over all dimension),
hence `item` is specified.

Save the above content in `torchlambda.yaml`.

## 3. Create deployment code

Now that we have our settings we can generate C++ code based on it.
Run the following:

```shell
$ torchlambda template --yaml torchlambda.yaml
```

You should see a new folder called `torchlambda` in your current directory
with `main.cpp` file inside.

__If you don't care about C++ you can move on to the next section.
If you want to know a little more (or your deployment needs more customization), carry on reading.__

If `YAML` settings cannot fulfil your needs `torchlambda`
offers you a basic `C++ template` you can start your deployment code from.

Run this simple command (no settings needed in this case):

```shell
$ torchlambda template --destination custom_deployment
```

This time you can find new folder `custom_deployment` with `main.cpp` inside.
This file is a minimal reasonable and working C++ code one should be able to follow
easily. It does exactly the same thing (except dynamic shapes) as we did above
via settings but this time the file is readable (previous `main.cpp` might be quite hard to grasp
as it's "autogenerated").

<details>

  __<summary> Click here to check generated code</summary>__

```cpp
#include <aws/core/Aws.h>
#include <aws/core/utils/base64/Base64.h>
#include <aws/core/utils/json/JsonSerializer.h>
#include <aws/core/utils/memory/stl/AWSString.h>

#include <aws/lambda-runtime/runtime.h>

#include <torch/script.h>
#include <torch/torch.h>

/*!
 *
 *                    HANDLE REQUEST
 *
 */

static aws::lambda_runtime::invocation_response
handler(torch::jit::script::Module &module,
        const Aws::Utils::Base64::Base64 &transformer,
        const aws::lambda_runtime::invocation_request &request) {

  const Aws::String data_field{"data"};

  /*!
   *
   *              PARSE AND VALIDATE REQUEST
   *
   */

  const auto json = Aws::Utils::Json::JsonValue{request.payload};
  if (!json.WasParseSuccessful())
    return aws::lambda_runtime::invocation_response::failure(
        "Failed to parse input JSON file.", "InvalidJSON");

  const auto json_view = json.View();
  if (!json_view.KeyExists(data_field))
    return aws::lambda_runtime::invocation_response::failure(
        "Required data was not provided.", "InvalidJSON");

  /*!
   *
   *          LOAD DATA, TRANSFORM TO TENSOR, NORMALIZE
   *
   */

  const auto base64_data = json_view.GetString(data_field);
  Aws::Utils::ByteBuffer decoded = transformer.Decode(base64_data);

  torch::Tensor tensor =
      torch::from_blob(decoded.GetUnderlyingData(),
                       {
                           static_cast<long>(decoded.GetLength()),
                       },
                       torch::kUInt8)
          .reshape({1, 3, 64, 64})
          .toType(torch::kFloat32) /
      255.0;

  torch::Tensor normalized_tensor = torch::data::transforms::Normalize<>{
      {0.485, 0.456, 0.406}, {0.229, 0.224, 0.225}}(tensor);

  /*!
   *
   *                      MAKE INFERENCE
   *
   */

  auto output = module.forward({normalized_tensor}).toTensor();
  const int label = torch::argmax(output).item<int>();

  /*!
   *
   *                       RETURN JSON
   *
   */

  return aws::lambda_runtime::invocation_response::success(
      Aws::Utils::Json::JsonValue{}
          .WithInteger("label", label)
          .View()
          .WriteCompact(),
      "application/json");
}

int main() {
  /*!
   *
   *                        LOAD MODEL ON CPU
   *                    & SET IT TO EVALUATION MODE
   *
   */

  torch::NoGradGuard no_grad_guard{};
  constexpr auto model_path = "/opt/model.ptc";

  torch::jit::script::Module module = torch::jit::load(model_path, torch::kCPU);
  module.eval();

  /*!
   *
   *                        INITIALIZE AWS SDK
   *                    & REGISTER REQUEST HANDLER
   *
   */

  Aws::SDKOptions options;
  Aws::InitAPI(options);
  {
    const Aws::Utils::Base64::Base64 transformer{};
    const auto handler_fn =
        [&module,
         &transformer](const aws::lambda_runtime::invocation_request &request) {
          return handler(module, transformer, request);
        };
    aws::lambda_runtime::run_handler(handler_fn);
  }
  Aws::ShutdownAPI(options);
  return 0;
}
```

</details>

For more info run `torchlambda template --help` or
[check out documentation](https://github.com/szymonmaszke/torchlambda/wiki/Commands#torchlambda-template).

## 4. Package your source as .zip

Now we have our model and source code. It's time to deploy it as AWS Lambda
ready `.zip` package.

Run from command line:

```shell
$ torchlambda build ./torchlambda --compilation "-Wall -O2"
```

Above will create `torchlambda.zip` file ready for deploy.
Notice `--compilation` where you can pass any [C++ compilation flags](https://gcc.gnu.org/onlinedocs/gcc/Option-Summary.html) (here `-O2`
for increased performance).

There are many more things one could set during this step, check `torchlambda build --help`
or [documentation](https://github.com/szymonmaszke/torchlambda/wiki/Commands#torchlambda-build)
for full list of available options and description.

## 5. Package your model as AWS Lambda Layer

Our source code is roughly `30Mb` in size (AWS Lambda has `250Mb` limit),
hence we can put our model as additional layer (so AWS S3 won't be involved).
To create it run:

```shell
$ torchlambda layer ./model.ptc --destination "model.zip"
```

You will receive `model.zip` layer in your current working directory (`--destination` is optional).
See `torchlambda layer --help` or [documentation](https://github.com/szymonmaszke/torchlambda/wiki/Commands#torchlambda-layer) for more info.

## 6. Deploy to AWS Lambda

From now on you could mostly follow tutorial from [AWS Lambda's C++ Runtime](https://github.com/awslabs/aws-lambda-cpp).
It is assumed you have AWS CLI configured, check [Configuring the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html) otherwise
(or see [Test Lambda deployment locally](https://github.com/szymonmaszke/torchlambda/wiki/Test-Lambda-deployment-locally) tutorial)

### 6.1 Create trust policy JSON file

First create the following trust policy JSON file:

```shell
$ cat trust-policy.json
{
 "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": ["lambda.amazonaws.com"]
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

### 6.2 Create IAM role trust policy JSON file

Run from your shell:

```shell
$ aws iam create-role --role-name demo --assume-role-policy-document file://trust-policy.json
```

Note down the role `Arn` returned to you after running that command, it will be needed during next step.

### 6.3 Create AWS Lambda function

Create deployment function with the script below:

```shell
$ aws lambda create-function --function-name demo \
  --role <specify role arn from step 5.2 here> \
  --runtime provided --timeout 30 --memory-size 1024 \
  --handler torchlambda --zip-file fileb://torchlambda.zip
```

### 6.4 Create AWS Layer containing model

We already have our `ResNet18` packed appropriately so run the following to make a layer
from it:

```shell
$ aws lambda publish-layer-version --layer-name model \
  --description "Resnet18 neural network model" \
  --license-info "MIT" \
  --zip-file fileb://model.zip
```

Please save the `LayerVersionArn` just like in `6.2` and insert below to add this layer
to function from previous step:

```shell
$ aws lambda update-function-configuration \
  --function-name demo \
  --layers <specify layer arn from above here>
```

This configures whole deployment, now we our model is ready to get incoming requests.

## 7. Send image as request to Lambda

Following script (save it as `request.py`) will send image-like `tensor` encoded using `base64`
via `aws lambda invoke` to test our function.

```python
import argparse
import base64
import shlex
import struct
import subprocess
import sys

import numpy as np


def parse_arguments():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("function-name")
    parser.add_argument("channels", type=int)
    parser.add_argument("width", type=int)
    parser.add_argument("height", type=int)
    parser.add_argument("output", type=int)

    return parser.parse_args()


def request(args):
    # Input should always be flattened!
    random_image = (
        np.random.randint(
            low=0, high=255, size=(1, args.channels, args.width, args.height)
        )
        .flatten()
        .tolist()
    )
    command = (
        """aws lambda invoke --function-name {} --payload"""
        """'{{"data": "{}", "channels": {}, "width": {}, "height": {} }}' {}""".format(
            args.function_name,
            args.channels,
            args.width,
            args.height,
            random_image
            args.output,
        )
    )

    subprocess.call(shlex.split(command))


if __name__ == "__main__":
    args = parse_arguments()
    request(args)
```

Run above script:

```shell
$ python request.py demo 3 64 64 output.json
```

You should get the following response in `output.json` (your label may vary):

```shell
cat output.txt
  {"label": 40}
```

__Congratulations, you have deployed ResNet18 classifier using only AWS Lambda in 7 steps__!


# Contributing

If you find issue or would like to see some functionality (or implement one), please [open new Issue](https://help.github.com/en/articles/creating-an-issue) or [create Pull Request](https://help.github.com/en/articles/creating-a-pull-request-from-a-fork).

#### Footnotes

<a name="footnote1">1</a>. Support for latest version of it's main DL framework or main frameworks if multiple
supported

<a name="footnote2">2</a>. Project dependencies shape can be easily cutomized. In torchlambda case it is customizable
build of [`libtorch`](https://pytorch.org/cppdocs/) and [`AWS C++ SDK`](https://aws.amazon.com/sdk-for-cpp/)

<a name="footnote2">3</a>. Necessary size of code and dependencies to deploy model

<a name="footnote2">4</a>. Based on [Dockerfile size](https://hub.docker.com/r/tensorflow/serving)
