
[![Go Report Card](https://goreportcard.com/badge/github.com/yaacov/kubesql)](https://goreportcard.com/report/github.com/yaacov/kubesql)
[![Build Status](https://travis-ci.org/yaacov/kubesql.svg?branch=master)](https://travis-ci.org/yaacov/kubesql)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

<p align="center">
  <img src="https://raw.githubusercontent.com/yaacov/kubesql/master/img/kubesql-162.png" alt="kubesql Logo">
</p>

# kubesql

Use SQL like language to query the [Kubernetes](https://kubernetes.io/) cluster manager

  - [Install](#install)
  - [What does it do ?](#what-does-it-do-)
    - [Operators](#available-operators)
    - [Math Operators](#available-math-operators)
    - [Aliases](#aliases)
    - [SI Units](#si-units)
    - [Formats](#output-formats)
    - [Arrays](#arrays-and-lists)
    - [Escapingg](#identifier-escaping)
  - [Examples](#examples)
    - [All Namespaces](#all-namespaces)
    - [Regexp](#using-regexp)
    - [Compere Fields](#comparing-fields)
    - [Print Help](#print-help)
  - [Config File](#config-file)
  - [Query language](#query-language)
  - [Alternatives](#alternatives)
    - [jq](#jq)
    - [Field Selector](#kubectl---field-selector)


<p align="center">
   <a href="https://asciinema.org/a/bU45k4co934j6DYW85NtiMGAl" target="_blank"><img src="https://asciinema.org/a/bU45k4co934j6DYW85NtiMGAl.svg" width="400"/></a>
<p>
  
## Install

Using `go get` command:
``` bash
GO111MODULE=on go get -v github.com/yaacov/kubesql/cmd/kubesql
```

Using Fedora Copr:

```
dnf copr enable yaacov/kubesql
dnf install kubesql
```

From source:

``` bash
git clone git@github.com:yaacov/kubesql.git
cd kubesql

make
```
  
## What does it do ?

kubesql let you select Kubernetes resources based on the value of one or more resource fields, using
human readable easy to use SQL like query langauge.

Example:
``` bash
# Filter replica sets with less ready-replicas then replicas"
kubesql --all-namespaces get rs where "status.readyReplicas < status.replicas"
```

For other ways to select Kubernetes resources see [#Alternatives](https://github.com/yaacov/kubesql#alternatives).

#### Available Operators:

| Opertors | Example |
|----|---|
| `=`, `~=` | `name ~= '^test-'`  |
| `like`, `ilike` | `phase ilike 'run%'`  | 
|`!=`, `!~` |  `namespace != 'default'` |
|`>`, `<`, `<=` and `>=` | `created < 2020-01-15T00:00:00Z` |
|`is null`, `is not null`| `spec.domain.cpu.dedicatedCpuPlacement is not null` |
| `in`   |  `spec.domain.resources.limits.memory in (1Gi, 2Gi)` |
| `between`   |  `spec.domain.resources.limits.memory between 1Gi and 2Gi` |
| `or`, `and` and `not` | `name ~= 'virt-' and namespace != 'test-wegsb'` |
| `( )`|  `phase = 'Running' and (namespace ~= 'cnv-' or namespace ~= 'virt-')`|

#### Available Math Operators:

| Opertors | Notes |
|----|---|
| `+`, `-` | Adition and Substruction |
| `*`, `/` | Multiplation and Division |
| `( )`|  |

#### Aliases:
| Aliase | Resource Path | Example |
|----|---|---|
| name | metadata.name | |
| namespace | metadata.namespace | `namespace ~= '^test-[a-z]+$'` |
| labels | metadata.labels | |
| annotations | metadata.annotations | |
| created | creation timestamp | |
| deleted | deletion timestamp | |
| phase | status.phase | `phase = 'Running'` |

#### SI Units:
| Unit | Multiplier | Example |
|----|---|---|
| Ki | 1024 | |
| Mi | 1024^2 | `spec.containers.1.resources.requests.memory = 200Mi` |
| Gi | 1024^3 | |
| Ti | 1024^4 | |
| Pi | 1024^5 | |

#### Booleans:
| Example |
|---|
| `status.conditions.1.status = true` |

#### RFC3339 dates:
| Example |
|---|
| `status.conditions.1.lastTransitionTime > 2020-02-20T11:12:38Z`  |

#### Output formats:
| --output flag | Print format |
|----|---|
| table | Table |
| name | Names onlly |
| yaml | YAML |
| json | JSON |

#### Arrays and lists:
kubesql support resource paths that include lists by using the list index as a field key.

``` bash
# Get the memory request for the first container.
kubesql --all-namespaces get pods where "spec.containers.1.resources.requests.memory = 200Mi"
```

#### Identifier escaping

If identifier include characters that need escaping ( e.g. "-" or ":") it is posible
to escape the identifier name by wrapping it with `[...]` , `` `...` `` or `"..."`

## Examples

#### All namespaces

``` bash
# Get pods that hase name containing "ovs"
kubesql --all-namespaces get pods where "name ~= 'ovs'"
AMESPACE    	NAME               	PHASE  	hostIP        	CREATION_TIME(RFC3339)       	
openshift-cnv	ovs-cni-amd64-5vgcg	Running	192.168.126.58	2020-02-10T23:26:31+02:00    	
openshift-cnv	ovs-cni-amd64-8ts4w	Running	192.168.126.12	2020-02-10T22:01:59+02:00    	
openshift-cnv	ovs-cni-amd64-d6vdb	Running	192.168.126.53	2020-02-10T23:13:45+02:00
...
```

#### Using Regexp

``` bash
# Get all pods from current namespace scope, that has a name starting with "virt-" and
# IP that ends with ".84"
kubesql get pods where "name ~= '^virt-' and status.podIP ~= '[.]84$'"
AMESPACE	NAME                          	PHASE  	hostIP        	CREATION_TIME(RFC3339)       	
default  	virt-launcher-test-bdw2p-lcrwx	Running	192.168.126.56	2020-02-12T14:14:01+02:00
...
```
#### SI Units

``` bash
# Get all persistant volume clames that are less then 20Gi, and output as json.
kubesql -o json get pvc where "spec.resources.requests.storage < 20Gi"

... 
{
  "storage": "10Gi"
}
...
```

#### Comparing fields

``` bash
# Get replicas sets with 3 replicas but less ready relicas
kubesql --all-namespaces get rs where "spec.replicas = 3 and status.readyReplicas < spec.replicas"

...
```
#### Print help

```
kubesql --help
...
```

## Config File

Users can add aliases and edit the fields displayed in table view using json config files,
[see the example config file](https://github.com/yaacov/kubesql/blob/master/config.example.json).

## Query language

kubesql uses Tree Search Language (TSL). TSL is a wonderful human readable filtering language.

https://github.com/yaacov/tree-search-language

## Alternatives

#### jq

`jq` is a lightweight and flexible command-line JSON processor. It is posible to
pipe the kubectl command output into the `jq` command to create complicted searches.

https://stedolan.github.io/jq/manual/#select(boolean_expression)

#### kubectl --field-selector

Field selectors let you select Kubernetes resources based on the value of one or more resource fields. Here are some examples of field selector queries.

https://kubernetes.io/docs/concepts/overview/working-with-objects/field-selectors/
