<!--- Heading --->
<div align="center">
  <h1>ak_cache</h1>
  <p>
    Cache any data for your python projects
  </p>
<h4>
    <a href="https://github.com/rpakishore/ak_cache/">View Demo</a>
  <span> · </span>
    <a href="https://github.com/rpakishore/ak_cache">Documentation</a>
  <span> · </span>
    <a href="https://github.com/rpakishore/ak_cache/issues/">Report Bug</a>
  <span> · </span>
    <a href="https://github.com/rpakishore/ak_cache/issues/">Request Feature</a>
  </h4>
</div>
<br />

![GitHub commit activity](https://img.shields.io/github/commit-activity/m/rpakishore/ak_cache)
![GitHub last commit](https://img.shields.io/github/last-commit/rpakishore/ak_cache)
<!-- Table of Contents -->
<h2>Table of Contents</h2>

- [1. About the Project](#1-about-the-project)
  - [1.1. Features](#11-features)
- [2. Getting Started](#2-getting-started)
  - [2.1. Prerequisites](#21-prerequisites)
  - [2.2. Installation](#22-installation)
- [3. Usage](#3-usage)
- [4. Roadmap](#4-roadmap)
- [5. License](#5-license)
- [6. Contact](#6-contact)
- [7. Acknowledgements](#7-acknowledgements)

<!-- About the Project -->
## 1. About the Project

<!-- Features -->
### 1.1. Features

- Read and write data to a Cached Pickle File

<!-- Getting Started -->
## 2. Getting Started

<!-- Prerequisites -->
### 2.1. Prerequisites

<!-- Installation -->
### 2.2. Installation

Install my-project with flit

```bash
git clone https://github.com/rpakishore/ak_cache.git
cd ak_cache
pip install flit
flit install
```

Alternatively, you can use pip

```bash
pip install ak_cache
```

<!-- Usage -->
## 3. Usage

Use this space to tell a little more about your project and how it can be used. Show additional screenshots, code samples, demos or link to other resources.

```python
$ from ak_cache import Cache
$ cache_file = Cache(r'Path\to\Cache\file.pkl')
$ cache_file.write('This is a text')
$ cache_file.read()
'This is a text'
```

Encrypt your pickle file as below

```python
$ cache_file = Cache(r'Path\to\Cache\encr_file.pkl', password="Strong_Password")

$ cache_file.write('This is an encrypted text')
$ cache_file.read()
'This is an encrypted text'
```
<!-- Roadmap -->
## 4. Roadmap

- [x] Add encryption option to the cache file

<!-- License -->
## 5. License

See LICENSE.txt for more information.

<!-- Contact -->
## 6. Contact

Arun Kishore - [@rpakishore](mailto:rpakishore@gmail.com)

Project Link: [https://github.com/rpakishore/](https://github.com/rpakishore/ak_cache)

<!-- Acknowledgments -->
## 7. Acknowledgements

Use this section to mention useful resources and libraries that you have used in your projects.

- [Awesome README Template](https://github.com/Louis3797/awesome-readme-template/blob/main/README-WITHOUT-EMOJI.md)
- [Banner Maker](https://banner.godori.dev/)
- [Shields.io](https://shields.io/)
- [Carbon](https://carbon.now.sh/)