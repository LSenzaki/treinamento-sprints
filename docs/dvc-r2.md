# DVC com Cloudflare R2

Este projeto usa `DVC` para versionar o arquivo `dataset_vendas.csv` fora do GitHub.

## 1. Criar o remote no projeto

Substitua os valores abaixo pelos do seu bucket:

```bash
dvc remote add -d storage s3://<bucket>/<prefixo-opcional>
dvc remote modify storage endpointurl https://<account-id>.r2.cloudflarestorage.com
dvc remote modify storage access_key_id <R2_ACCESS_KEY_ID>
dvc remote modify storage secret_access_key <R2_SECRET_ACCESS_KEY> --local
```

Notas:

- O `endpointurl` do R2 usa o `account-id` da sua conta Cloudflare.
- O `secret_access_key` deve ficar com `--local` para nao ser commitado.
- Se preferir, voce tambem pode salvar `access_key_id` com `--local`.

## 2. Publicar o dataset no remote

Depois de configurar o remote:

```bash
dvc push
```

Isso envia o conteudo real do `dataset_vendas.csv` para o R2.

## 3. Baixar os dados em outra maquina

Depois de clonar o repositorio e configurar as credenciais:

```bash
dvc pull
```

## 4. Atualizar o dataset no futuro

Quando o CSV mudar:

```bash
dvc add dataset_vendas.csv
git add dataset_vendas.csv.dvc .gitignore .dvc .dvcignore
git commit -m "chore: update dataset tracking"
dvc push
git push
```
