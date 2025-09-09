# Crackling Cloud (using Amazon Web Services)

[Crackling](https://github.com/bmds-lab/Crackling) is one of the leading CRISPR-Cas9 guide RNA design tools. 

In this implementation of Crackling, we use generally-available computing technologies by Amazon Web Services (AWS) so anyone can design high-quality gRNA without needing a supercomputer/HPC, nor having to send their data to a third-party.

With thanks to our colleagues at the CSIRO for their support during the development of this edition of the pipeline.

For support, contact Jake Bradford.

## As seen at...

**The International Conference for High Performance Computing, Networking, Storage, and Analysis (Supercomputing) 2024**

... in the Workshop: "WHPC: Diversity and Inclusion for All" ([abstract](https://sc24.supercomputing.org/proceedings/workshops/workshop_pages/ws_whpc124.html))

*Event-driven high-performance cloud computing for CRISPR-Cas9 guide RNA design*

Divya Joy<sup>1</sup>, Jacob Bradford<sup>1</sup>

<sup>1</sup> Queensland University of Technology, Brisbane, Australia 

**The Annual Conference of the Australian Bioinformatics and Computational Biology Society 2020**

*CRISPR, faster, better - The Crackling method for whole-genome target detection*

Jacob Bradford<sup>1</sup>, Timothy Chappell<sup>1</sup>, Brendan Hosking<sup>2</sup>, Laurence Wilson<sup>2</sup>, Dimitri Perrin<sup>1</sup>


<sup>1</sup> Queensland University of Technology, Brisbane, Australia 

<sup>2</sup> Commonwealth Scientific and Industrial Research Organisation (CSIRO), Sydney, Australia 

## Please cite us

Please cite our paper when using Crackling:

> Bradford, J., Joy, D., Winsen, M., Meurant, N., Wilkins, M., Wilson, L., Bauer, D., & Perrin, D. (2024). Crackling Cloud: an event-driven, cloud-based CRISPR-Cas9 guide RNA design tool. bioRxiv, 2024-12.

> Bradford, J., Chappell, T., & Perrin, D. (2022). *Rapid whole-genome identification of high quality CRISPR guide RNAs with the Crackling method.* The CRISPR Journal, 5(3), 410-421.

The standalone implementation is available on GitHub, [here](https://github.com/bmds-lab/Crackling).

# Deploy from GitHub Actions

This guide explains how to deploy the **Crackling-AWS** application using GitHub Actions. The workflow will make the software available in your AWS account.

## Step 1: Create an AWS Account

If you don't already have an AWS account, sign up at [https://aws.amazon.com/](https://aws.amazon.com/) and complete the account setup process.

## Step 2: Fork the Repository

1. Go to the Crackling-AWS GitHub repository.
2. Click the **Fork** button at the top-right corner.

## Step 3: Set Up GitHub Secrets and Variables

The workflow requires your AWS credentials and configuration:

1. Go to your forked repository on GitHub.
2. Navigate to **Settings → Secrets and variables → Actions → Secrets**.
3. Add the following secrets:

   * `AWS_ACCESS_KEY_ID` – Your AWS access key ID
   * `AWS_SECRET_ACCESS_KEY` – Your AWS secret access key
   * `AWS_SESSION_TOKEN` – (Optional) Only if using temporary credentials

4. Add the following repository variables:

   * `AWS_REGION` – The AWS region to deploy resources (e.g., `ap-southeast-2`)
   * `AWS_STACK_NAME` – The name you want for your CloudFormation stack (e.g., `CracklingStack`)

## Step 4: Start the Deployment

Once the secrets and variables are set:

1. Go to the **Actions** tab in your forked repository.
2. Select the workflow **Deploy Crackling-AWS**.
3. Click **Run workflow**.
4. Wait for the workflow to complete. You can see the progress in real time. It might take about 15 minutes.

## Step 5: Verify Deployment

After the workflow finishes, it will generate two links. One for the web application that you use to start the guide design process, and another for a back-end access (the API; for advanced users only).

Optionally, check your AWS account to confirm resources are created (Lambda, S3, DynamoDB, SQS, etc.).

## Step 6: Access Crackling Cloud

Access your deployment of Crackling Cloud using the generated URLs:

    - The CloudFront URL provides you access to a simple web interface to submit jobs and retrieve results.

    - The API endpoint URL provides you access to same features of the web interface but allows you to write custom scripts or use third-party tools to interface with your deployment of Crackling Cloud.

   For example,

   ```
    CloudfrontURL: d123q1z2zzz999.cloudfront.net
	
    CracklingRestApiEndpoint: https://e123456789.execute-api.ap-southeast-2.amazonaws.com/prod/
   ```

## Step 7: Run a test job

Submit a job with these details (provided as defaults):

   **Query sequence:**

   ```
   ATCGATCGATCGATCGATCGAGGATCGATCGATCGATCGATCGTGGCCAATCGATCGATCGATCGATCG
   ```

   **Genome Accession:**

   ```
   GCA_000482205.1
   ```

Try a larger job, designing guides for the TFL1 gene of Arabidopsis Thaliana.

   **Query sequence:**

   ```
   AAATAGATGTCTCGGTCGTCTCTTTGTCTCCCAAATCACTACAAATCTCTCTTTTCCTCTAAGTTAACAAAAGAAAATGGAGAATATGGGAACTAGAGTGATAGAGCCATTGATAATGGGGAGAGTGGTAGGAGATGTTCTTGATTTCTTCACTCCAACAACTAAGATGAATGTTAGTTATAACAAGAAGCAAGTCTCCAATGGCCATGAGCTCTTTCCTTCTTCTGTTTCCTCCAAGCCTAGGGTTGAGATCCATGGTGGTGATCTCAGATCCTTCTTCACTTTGGTGATGATAGACCCAGATGTTCCAGGTCCTAGTGACCCCTTTCTAAAAGAACACCTGCACTGGATCGTTACAAACATTCCCGGCACAACAGATGCTACGTTTGGCAAAGAGGTGGTGAGCTATGAATTGCCAAGGCCAAGCATAGGGATACATAGGTTTGTGTTTGTTCTGTTCAGGCAGAAGCAAAGACGTGTTATCTTTCCTAATATCCCTTCGAGAGATCACTTCAACACTCGTAAATTTGCGGTCGAGTATGATCTTGGTCTCCCTGTCGCGGCCGTCTTCTTTAACGCACAAAGAGAAACCGCTGCACGCAAACGCTAGTTTCATGATTGTCATAAACTGCAAAAATGAAAGAAGAAAATTTGCATGTAATCTCATGTTTATTTGTGTTCTGAATTTCCGTACTCTGAATAAAAACTGCCAAAGATGAGTTGAATCCGAAATATCAATTGAGTTTACAGAAGTATTGATAACGATCTGTCGATTATCAGAATAAAAACTAGATTAATTGCATATCATGTTTAGCATTGTAATACTACAAAAATAGTAAACTCTTGATTAATTAATAAAATCTAAGTTGC
   ```

   **Genome Accession:**

   ```
   GCF_000001735.4
   ```


## Step 8: Inspect results

After submitting the job, the interface will automatically switch to the 'retrieve results' tab. Click on the green 'Retrieve Results' button, progressively, until all results are ready. The status indicator will how analysis is progressing:


    ```
    Identified 3 candidate guides
    Completed efficiency evaluation for 0 guides
    Completed specificity evaluation for 0 guides
    ```

    The sample inputs will generate three guide RNA. 

    - Start, end and strand describe where the guide RNA are found along the input gene sequence.

    - The guide RNA itself is the sequence

    - Consensus results reflects the predictive efficiency of the guide RNA. See the 'About' tab for more information. You should use guides that have scored at least two out of three.

    - Off-target score reflects the predicted specificity of the guide RNA. See the 'About' tab for more information. You should use guides that have scored at least 75 out of 100. 
    


# Deploy from your local machine

This process is useful for developers. If you are wanting to design guides but not contribute to the development of Crackling-AWS, then this is not the option for you.\

Note to developers: the GitHub workflow best describes the deployment process.

## Step 1: Create an AWS account

If you do not have an AWS account, follow [this](https://aws.amazon.com/resources/create-account/) AWS user guide

## Step 2: Clone the repository

Use git to clone this repository, or download a Zip copy from GitHub.

## Step 3: Deploy the software

Follow the deployment instructions below.

## Step 4: Access Crackling Cloud

Access your deployment of Crackling Cloud using the generated URLs:

    - The CloudFront URL provides you access to a simple web interface to submit jobs and retrieve results.

    - The API endpoint URL provides you access to same features of the web interface but allows you to write custom scripts or use third-party tools to interface with your deployment of Crackling Cloud.

   For example,

   ```
    CloudfrontURL: d123q1z2zzz999.cloudfront.net
	
    CracklingRestApiEndpoint: https://e123456789.execute-api.ap-southeast-2.amazonaws.com/prod/
   ```

## Step 5: Run a test job

Submit a job with these details (provided as defaults):

    **Query sequence:**

   ```
   ATCGATCGATCGATCGATCGAGGATCGATCGATCGATCGATCGTGGCCAATCGATCGATCGATCGATCG
   ```

   **Genome Accession:**

   ```
   GCA_000482205.1
   ```

## Step 6: Inspect results

After submitting the job, the interface will automatically switch to the 'retrieve results' tab. Click on the green 'Retrieve Results' button, progressively, until all results are ready. The status indicator will how analysis is progressing:


    ```
    Identified 3 candidate guides
    Completed efficiency evaluation for 0 guides
    Completed specificity evaluation for 0 guides
    ```

    The sample inputs will generate three guide RNA. 

    - Start, end and strand describe where the guide RNA are found along the input gene sequence.

    - The guide RNA itself is the sequence

    - Consensus results reflects the predictive efficiency of the guide RNA. See the 'About' tab for more information. You should use guides that have scored at least two out of three.

    - Off-target score reflects the predicted specificity of the guide RNA. See the 'About' tab for more information. You should use guides that have scored at least 75 out of 100. 

# Architecture

![Architecture diagram](CracklingAws.drawio.png)

# Development instructions

**Be sure you have cloned this repository to your computer.**

**1. Install the AWS command-line interface**

Follow the AWS Documentation for [Getting started with the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html)

**2. Install the AWS Cloud Development Kit**

Follow the AWS Documentation for [Getting started with the AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html)

**3. Shared objects (for binaries)**

Collect all shared objects needed by compiled binaries.

See here: https://www.commandlinefu.com/commands/view/10238/copy-all-shared-libraries-for-a-binary-to-directory

Working in the root directory of the repo, run:

```bash
ldd layers/isslScoreOfftargets/isslScoreOfftargets | grep "=> /" | awk '{print $3}' | xargs -I '{}' cp -v '{}' layers/sharedObjects
```

then

```bash
ldd layers/rnaFold/rnaFold/RNAfold | grep "=> /" | awk '{print $3}' | xargs -I '{}' cp -v '{}' layers/sharedObjects
```

**4. Python Modules **

The `pip install -r' command is used frequently throught the following section. In some enviroments, this command errors out. If this occours, please view the requirments.txt file (referenced in the command) and use pip to install each library manually.

**GenomePartsDownloader Layer**

Working in the root directory of the repository, run:

```bash
mkdir -p ./layers/requestsPy310Pkgs/python
python3 -m pip install --target layers/requestsPy310Pkgs/python requests
```

**NCBI Layer:**

Working in the root directory of the repo, run:
```bash
mkdir -p layers/ncbi/python
python3 -m pip install --target layers/ncbi/python -r layers/requirements_ncbi.txt
```

**AWS App Modules**

Working in the `<root>/aws` directory:
```bash
python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

deactivate
```

**5. Further Reading**

Please now proceed to read the following documentation for futher install instructions (/understanding) for the application:
 - `<root>/layers/README.md`
 - `<root>/modules/README.md`
 - `<root>/aws/README.md`

**6. Deploying using the CDK**

Working from the `<root>/aws` directory:
```bash
# Run this during first deployment
cdk bootstrap aws://377188290550/ap-southeast-2
# Useful CDK commands include:
cdk synth # for creating the CloudFormation template without deploying
cdk deploy # for deploying the stack via CloudFormation
cdk destroy # for destroying the stack in CloudFormation
# add the `--profile` flag to indicate which set of AWS credentials you wish to use, e.g.  `--profile bmds`.
```
