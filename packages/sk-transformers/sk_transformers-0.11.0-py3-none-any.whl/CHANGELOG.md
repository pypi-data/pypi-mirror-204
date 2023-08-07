# Changelog

## [0.11.0](https://github.com/chrislemke/sk-transformers/compare/v0.10.3...v0.11.0) (2023-04-25)


### Features

* add StringCombinationTransformer ([#108](https://github.com/chrislemke/sk-transformers/issues/108)) ([48c6977](https://github.com/chrislemke/sk-transformers/commit/48c69777cd0ac6f11bf860457fe150d826c627fe))
* geo_distance_transformer ([#107](https://github.com/chrislemke/sk-transformers/issues/107)) ([2030569](https://github.com/chrislemke/sk-transformers/commit/2030569e549cffae923442537fb00cfed4098dc0))
* support python 11 ([#100](https://github.com/chrislemke/sk-transformers/issues/100)) ([d2cf4ae](https://github.com/chrislemke/sk-transformers/commit/d2cf4aee132767e30d8b2f6edc4eafdd208fa9da))


### Tests

* add # pragma: no cover ([02ae9c7](https://github.com/chrislemke/sk-transformers/commit/02ae9c7b7eee11651c65878005e3dd33a07afeeb))


### CI/CD

* pre-commit autoupdate ([#101](https://github.com/chrislemke/sk-transformers/issues/101)) ([0d224e7](https://github.com/chrislemke/sk-transformers/commit/0d224e76d832e0ab8d7793e06c315f5c54ee7836))
* pre-commit autoupdate ([#102](https://github.com/chrislemke/sk-transformers/issues/102)) ([dd2bb6b](https://github.com/chrislemke/sk-transformers/commit/dd2bb6b3ef143c2d18bb960ac6ee5aead549391f))
* pre-commit autoupdate ([#103](https://github.com/chrislemke/sk-transformers/issues/103)) ([f7c8732](https://github.com/chrislemke/sk-transformers/commit/f7c8732a7cf86644889735ad81a508b3fd1c259b))
* pre-commit autoupdate ([#104](https://github.com/chrislemke/sk-transformers/issues/104)) ([fd4173a](https://github.com/chrislemke/sk-transformers/commit/fd4173a66c252a1e6f0ab6668c44b5c6aee9ae00))
* pre-commit autoupdate ([#105](https://github.com/chrislemke/sk-transformers/issues/105)) ([238d99f](https://github.com/chrislemke/sk-transformers/commit/238d99f171c18f8fc1f27d8c086c1b55cb523e46))
* pre-commit autoupdate ([#112](https://github.com/chrislemke/sk-transformers/issues/112)) ([7c630ed](https://github.com/chrislemke/sk-transformers/commit/7c630eded06d3f1e0c92694ea61bee9db40e236f))


### Maintenance

* add support for `polars` ([#87](https://github.com/chrislemke/sk-transformers/issues/87)) ([b831485](https://github.com/chrislemke/sk-transformers/commit/b831485d0d857a5e0c4ec478e745697df0fb2eb9))
* replace static methods in some transformers ([#110](https://github.com/chrislemke/sk-transformers/issues/110)) ([fa6215d](https://github.com/chrislemke/sk-transformers/commit/fa6215de6db0e713865b6f46847f8219864295b4))
* series manipulation for ip to float ([#111](https://github.com/chrislemke/sk-transformers/issues/111)) ([39aa55a](https://github.com/chrislemke/sk-transformers/commit/39aa55afd3514c89c44b89cd4b8bc3f2e68a54c7))

## [0.10.3](https://github.com/chrislemke/sk-transformers/compare/v0.10.2...v0.10.3) (2023-03-10)


### Maintenance

* remove slots for compatibility reasons ([2a58219](https://github.com/chrislemke/sk-transformers/commit/2a58219e030447fbcb11476130f7a79bfd56a846))

## [0.10.2](https://github.com/chrislemke/sk-transformers/compare/v0.10.1...v0.10.2) (2023-03-09)


### Bug Fixes

* broken dependencies ([3fa0a19](https://github.com/chrislemke/sk-transformers/commit/3fa0a1979ec8858623f9297d2057674950dd71dc))

## [0.10.1](https://github.com/chrislemke/sk-transformers/compare/v0.10.0...v0.10.1) (2023-03-09)


### Features

* rich for better error messages ([9cd9569](https://github.com/chrislemke/sk-transformers/commit/9cd9569a30212b5577489d5fc16f7466ad2d6cb9))


### Bug Fixes

* make tuples flexible in string transformers ([#77](https://github.com/chrislemke/sk-transformers/issues/77)) ([b02ccdb](https://github.com/chrislemke/sk-transformers/commit/b02ccdb8f170441657a01f653c22e10635521d17))
* support for 2-arg np math functions in MathExpTrans ([#83](https://github.com/chrislemke/sk-transformers/issues/83)) ([52f2d17](https://github.com/chrislemke/sk-transformers/commit/52f2d1777ff4b1b2974d4727b0368f790ec1e4d4))
* warning implementation ([#80](https://github.com/chrislemke/sk-transformers/issues/80)) ([406862a](https://github.com/chrislemke/sk-transformers/commit/406862aeeb7d756a2a0f077356e8ac6d0d8ac1b5))


### Documentation

* fix missing training_objective in example notebook ([f8f5d2f](https://github.com/chrislemke/sk-transformers/commit/f8f5d2f7668e433916000f82bbc87658c51277ba))


### Security

* update dependencies due to security issue with ipython ([bc8d0f0](https://github.com/chrislemke/sk-transformers/commit/bc8d0f0ca933521613699fb7cccd6c98835431a9))


### CI/CD

* add pre-commit-hooks-safety ([5c50988](https://github.com/chrislemke/sk-transformers/commit/5c50988f95336dc8f34d7807358daa6c72ed2547))
* fix issue of double running release action ([d5ba926](https://github.com/chrislemke/sk-transformers/commit/d5ba926366aa3e0fd1851e9d389f6270ed4f2e7a))
* fix issue with autoupdate from pre-commit ([267bb03](https://github.com/chrislemke/sk-transformers/commit/267bb034e08d3bea98e07b3376fc8c8f74edb2ee))
* pre-commit autoupdate ([3699230](https://github.com/chrislemke/sk-transformers/commit/36992309db45ae820f59f909d0a05cc61c308bb6))
* update pre-commit ([c82aa1f](https://github.com/chrislemke/sk-transformers/commit/c82aa1f42155e55f79106537fb5c169c955bf6e7))


### Maintenance

* improve aggregate_transformer ([#79](https://github.com/chrislemke/sk-transformers/issues/79)) ([ae94ac0](https://github.com/chrislemke/sk-transformers/commit/ae94ac06317f3f0ece5bcd7a7c7a8b9a706da96a))
* remove deep_transformer module ([#92](https://github.com/chrislemke/sk-transformers/issues/92)) ([27687e8](https://github.com/chrislemke/sk-transformers/commit/27687e8c02bfa8b518167fa63e385a71fda3cb17))
* start using __slots__ ([#89](https://github.com/chrislemke/sk-transformers/issues/89)) ([0cb3f5a](https://github.com/chrislemke/sk-transformers/commit/0cb3f5a0236a966139cd81e752f54dd51774dee7))

## [0.10.0](https://github.com/chrislemke/sk-transformers/compare/v0.9.1...v0.10.0) (2023-01-26)


### Features

* add date columns transformer ([#68](https://github.com/chrislemke/sk-transformers/issues/68)) ([6e6ce3e](https://github.com/chrislemke/sk-transformers/commit/6e6ce3e305dc7a811e2867b4f7ab7605c54cc8f8))


### Bug Fixes

* add sliced string as a separate column ([#71](https://github.com/chrislemke/sk-transformers/issues/71)) ([743f617](https://github.com/chrislemke/sk-transformers/commit/743f61781f964bcbc481bb1fb47b0e7b878fda81))


### CI/CD

* pre-commit autoupdate ([#69](https://github.com/chrislemke/sk-transformers/issues/69)) ([6241a09](https://github.com/chrislemke/sk-transformers/commit/6241a09947fbbbcb6efc1da0043e7a1bfbe6001e))


### Maintenance

* check for different dtypes in nan transformer ([#72](https://github.com/chrislemke/sk-transformers/issues/72)) ([ffc11cb](https://github.com/chrislemke/sk-transformers/commit/ffc11cb5d17733663a0f8f8e87dac37fe3bc9f25))
* improve error messages by adding transformer name ([#70](https://github.com/chrislemke/sk-transformers/issues/70)) ([b03d46a](https://github.com/chrislemke/sk-transformers/commit/b03d46a6377cb233c143317c39ce80f75d562b87))

## [0.9.1](https://github.com/chrislemke/sk-transformers/compare/v0.9.0...v0.9.1) (2023-01-23)


### CI/CD

* add auto comment github action ([#58](https://github.com/chrislemke/sk-transformers/issues/58)) ([bed2782](https://github.com/chrislemke/sk-transformers/commit/bed2782594ac6881d4ac1f2e7643de4f293cf80b))
* improve github actions ([#64](https://github.com/chrislemke/sk-transformers/issues/64)) ([e1f07e1](https://github.com/chrislemke/sk-transformers/commit/e1f07e1b41e1ae81c72b7306c6323a54ff9d0319))

## [0.9.0](https://github.com/chrislemke/sk-transformers/compare/v0.8.0...v0.9.0) (2023-01-20)


### Features

* add ColumnEvalTransformer ([#52](https://github.com/chrislemke/sk-transformers/issues/52)) ([a03b079](https://github.com/chrislemke/sk-transformers/commit/a03b079d1818674c7115b4f3122656f0f1af1b1d))
* add string_splitter_transformer ([#53](https://github.com/chrislemke/sk-transformers/issues/53)) ([fdf89e1](https://github.com/chrislemke/sk-transformers/commit/fdf89e1dd9cb9de1348a9be11796a24023ec1817))


### Bug Fixes

* allow nans in query transformer ([b8bf874](https://github.com/chrislemke/sk-transformers/commit/b8bf8748124b12f634182af5660875f3b98e397c))


### Maintenance

* improve data check by only checking used columns ([#54](https://github.com/chrislemke/sk-transformers/issues/54)) ([ca450a4](https://github.com/chrislemke/sk-transformers/commit/ca450a4d69d0b9136996edf3dedb8a7e51b148d7))


### CI/CD

* add ability to run the Release action manually ([#56](https://github.com/chrislemke/sk-transformers/issues/56)) ([42f76a3](https://github.com/chrislemke/sk-transformers/commit/42f76a318e1202c6556b4b7f335cb855ec30368a))

## [0.8.0](https://github.com/chrislemke/sk-transformers/compare/v0.7.4...v0.8.0) (2023-01-18)


### Features

* add allowed_values_transformer ([#46](https://github.com/chrislemke/sk-transformers/issues/46)) ([2fe06f6](https://github.com/chrislemke/sk-transformers/commit/2fe06f6ebd688faa7bba7fb3a51b431fa4f83040))


### Documentation

* fix broken url ([a1279b4](https://github.com/chrislemke/sk-transformers/commit/a1279b4a6116f8580149070e6bde1231b0747971))


### Maintenance

* add init file for easier usage of transformers ([#45](https://github.com/chrislemke/sk-transformers/issues/45)) ([e1edb18](https://github.com/chrislemke/sk-transformers/commit/e1edb18c4a184e771de577eca6ab24c77fe38339))

## [0.7.4](https://github.com/chrislemke/sk-transformers/compare/v0.7.3...v0.7.4) (2023-01-16)


### Bug Fixes

* allow nan in some transformers ([#41](https://github.com/chrislemke/sk-transformers/issues/41)) ([d2a4fbf](https://github.com/chrislemke/sk-transformers/commit/d2a4fbff12bba82c0cc0077673f8ee5d3a6fcca9))


### Maintenance

* add more pre-commit hooks ([#40](https://github.com/chrislemke/sk-transformers/issues/40)) ([b716c44](https://github.com/chrislemke/sk-transformers/commit/b716c44693666fc64d30a1d15f861de6ab66d8d3))


### CI/CD

* add fast-forward merge action to pull requests ([#42](https://github.com/chrislemke/sk-transformers/issues/42)) ([41036b9](https://github.com/chrislemke/sk-transformers/commit/41036b95ec4f6af29844409b467deb17f597b92c))

## [0.7.3](https://github.com/chrislemke/sk-transformers/compare/v0.7.2...v0.7.3) (2023-01-12)


### Bug Fixes

* deep transformer check ready to transform fails ([91f9712](https://github.com/chrislemke/sk-transformers/commit/91f97120d04f724c0df9b6a9fb42b16d9bda5a28))
* issue with failing check_array if dataframe contains objects and nan ([b99a734](https://github.com/chrislemke/sk-transformers/commit/b99a7345d9fd2ac875e0576961cdb4f024b755b1))

## [0.7.2](https://github.com/chrislemke/sk-transformers/compare/v0.7.1...v0.7.2) (2023-01-10)


### Maintenance

* add training_objective argument to tovectransformer ([#36](https://github.com/chrislemke/sk-transformers/issues/36)) ([041f11f](https://github.com/chrislemke/sk-transformers/commit/041f11fd42437cae058c018b84b00455a705f175))

## [0.7.1](https://github.com/chrislemke/sk-transformers/compare/v0.7.0...v0.7.1) (2023-01-06)


### Documentation

* fix icon issue in readme.md ([2371493](https://github.com/chrislemke/sk-transformers/commit/237149335a1a7cc7453609ee4784a6cfbf606da9))

## [0.7.0](https://github.com/chrislemke/sk-transformers/compare/v0.6.3...v0.7.0) (2023-01-06)


### Features

* add left_join_transformer ([#29](https://github.com/chrislemke/sk-transformers/issues/29)) ([31fbde0](https://github.com/chrislemke/sk-transformers/commit/31fbde02aada7c81236d4775b9ccc7f29510ac2f))


### Bug Fixes

* add `numpy` as a possible prefix ([#31](https://github.com/chrislemke/sk-transformers/issues/31)) ([8fec7d3](https://github.com/chrislemke/sk-transformers/commit/8fec7d30b4ed8415b090182c7a27d09310f070a2))


### CI/CD

* fix code-cov action ([f2be192](https://github.com/chrislemke/sk-transformers/commit/f2be1920fb037a3b5e8e215347613035df4dd441))


### Maintenance

* general improvements ([85596c2](https://github.com/chrislemke/sk-transformers/commit/85596c2526accb6bda9e7e5efd959fbf8ea28588))
* use swifter to speed up pandas apply ([#28](https://github.com/chrislemke/sk-transformers/issues/28)) ([53684e9](https://github.com/chrislemke/sk-transformers/commit/53684e912fa752e0c2902e99b93fa45dacda2613))


### Documentation

* add new project logo ([#32](https://github.com/chrislemke/sk-transformers/issues/32)) ([93e277b](https://github.com/chrislemke/sk-transformers/commit/93e277b6b7c26e7fdb1919512bdc188b2d51254f))
* add playground notebook ([#30](https://github.com/chrislemke/sk-transformers/issues/30)) ([681eaf9](https://github.com/chrislemke/sk-transformers/commit/681eaf92e3cf41a9fb93b446b2b5c21877ddf5f1))

## [0.6.3](https://github.com/chrislemke/sk-transformers/compare/v0.6.2...v0.6.3) (2023-01-04)


### Features

* deep transformer module ([#24](https://github.com/chrislemke/sk-transformers/issues/24)) ([fd266cf](https://github.com/chrislemke/sk-transformers/commit/fd266cf10c629cc5c5d33528006480fd5094cc96))

## [0.6.2](https://github.com/chrislemke/sk-transformers/compare/v0.6.1...v0.6.2) (2022-12-22)


### Documentation

* improve contributing file ([3b5287b](https://github.com/chrislemke/sk-transformers/commit/3b5287b1cd326b65331b086b4d2c8275a3dd170a))


### CI/CD

* improve the release process ([096f3b2](https://github.com/chrislemke/sk-transformers/commit/096f3b2482688ab561bf3afa4b6d8b98e1736186))

## [0.6.1](https://github.com/chrislemke/sk-transformers/compare/v0.6.0...v0.6.1) (2022-12-22)


### Bug Fixes

* wrong formatting in readme.md ([425f4ed](https://github.com/chrislemke/sk-transformers/commit/425f4ed1cf173ffad7534dae035528bc2fa81072))


### Documentation

* improve the usability ([4190cd7](https://github.com/chrislemke/sk-transformers/commit/4190cd7c356b540e788dfe5930ab198a1c5a13fe))

## [0.6.0](https://github.com/chrislemke/sk-transformers/compare/v0.5.7...v0.6.0) (2022-12-22)


### Features

* add scripts to improve the release process 🚀 ([54a9dfe](https://github.com/chrislemke/sk-transformers/commit/54a9dfeda3c4448502206f5e3181f69da17df9a5))
