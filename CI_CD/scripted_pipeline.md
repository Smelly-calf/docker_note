# 脚本管道 Jenkinsfile

https://www.jenkins.io/doc/book/pipeline/jenkinsfile/#

使用脚本管道语法定义的 Jenkinsfile 实现 Pipline in SCM。

### 1.Jenkins file示例
将管道工作包裹在 node 块中，有两个目的：
- 通过将项目添加到Jenkins队列中来计划要运行的块中包含的步骤。执行程序在节点上自由后，这些步骤将立即运行。
- 创建一个工作区（特定于特定管道的目录），在该工作区中可以对从源代码管理中检出的文件进行处理。

  警告：根据您的Jenkins配置，一段时间不活动后，某些工作区可能不会自动清理。有关更多信息，请参见JENKINS-2111链接的票证和讨论。

```
// Jenkinsfile (Scripted Pipeline)
properties([ 8
    parameters([
        string(name: 'Greeting', defaultValue: 'Hello', description: 'How should I greet the world?')
    ]),
    
])
node {
    stage('Build') {
        sh 'make' 
        archiveArtifacts artifacts: '**/target/*.jar', fingerprint: true 
    }
    stage('Test') {
            /* `make check` returns non-zero on test failures,
             * using `true` to allow the Pipeline to continue nonetheless
             */
            sh 'make check || true' 
            junit '**/target/*.xml' 
    }
    stage('Deploy') {
            if (currentBuild.result == null || currentBuild.result == 'SUCCESS') { 
                sh 'make publish'
            }
    }
}
``` 
- 1  node 空 表示在任何可用的代理中执行 Pipeline .

- 2  stage 块不是必须，但在脚本管道中声明 stage 块可以在Jenkins UI界面看到每个stage的清晰视图。

- 3  构建是一个管道工作的开始，
    
     Jenkins 的 Pipeline 只是绑定项目开发生命周期多个阶段（构建、测试、部署），可能不是真正的构建什么的。
 

### 语法
#### 字符串插值
Jenkins Pipeline使用与Groovy相同的规则进行字符串插值。

只有双引号字符串支持插值字符串:
```
def username = 'Jenkins'
echo 'Hello Mr. ${username}'
echo "I said, Hello Mr. ${username}"
```

结果：
```
Hello Mr. ${username}
I said, Hello Mr. Jenkins
```
脚本管道代码片段生成器：https://snippet-generator.app/?description=properties&tabtrigger=fafafaf&snippet=fafafaf&mode=vscode


#### 内置环境变量

| 变量名 | 描述 |
| --- | --- |
| BUILD_ID | 和 BUILD_NUMBER 相同 |
| BUILD_TAG | 等于 jenkins-${JOB_NAME}-${BUILD_NUMBER} |
| BUILD_URL | 构建结果url |
| EXECUTOR_NUMBER | 唯一标识当前executor，可以在build executor status中看到，number从0开始 |
| JAVA_HOME | JDK PATH |
| JENKINS_URL | JENKINS家目录 |
| JOB_NAME | 组+pipeline名称：foo/bar |
| NODE_NAME | 当前运行的节点，默认master |
| WORKSPACE | 当前job工作空间绝对路径 |

引用环境变量的语法：
```
node {
    echo "Running ${env.BUILD_ID} on ${env.JENKINS_URL}"
}

```

#### 自定义环境变量
```
node {
    /* .. 代码片段 .. */
    withEnv(["PATH+MAVEN=${tool 'M3'}/bin"]) {
        sh 'mvn -B verify'
    }
}
```

#### 动态环境变量
```
node {
    /* .. 代码片段 .. */
     // Using returnStdout
    withEnv([
            CC = """${sh(
                 returnStdout: true,
                 script: 'echo "clang"'
             )}"""
            EXIT_STATUS = """${sh(
                            returnStatus: true,
                            script: 'exit 1'
                        )}"""
    ]) {
        sh 'mvn -B verify'
       }
}
```

#### 凭据
SSH User Private Key example：
```
withCredentials(bindings: [sshUserPrivateKey(credentialsId: 'jenkins-ssh-key-for-abc', \
                                             keyFileVariable: 'SSH_KEY_FOR_ABC', \
                                             passphraseVariable: '', \
                                             usernameVariable: '')]) {
  // some block
}
```
Certificate example:
```
withCredentials(bindings: [certificate(aliasVariable: '', \
                                       credentialsId: 'jenkins-certificate-for-xyz', \
                                       keystoreVariable: 'CERTIFICATE_FOR_XYZ', \
                                       passwordVariable: 'XYZ-CERTIFICATE-PASSWORD')]) {
  // some block
}
```
Groovy语法中单引号更安全，双引号安全性较低
```
node {
  withCredentials([string(credentialsId: 'mytoken', variable: 'TOKEN')]) {
    sh /* CORRECT */ '''
      set +x
      curl -H 'Token: $TOKEN' https://some.api/
    '''
  }
}
```

使用代码片段生成器生成 withCredentials 语句：
Using the Snippet Generator, you can make multiple credentials available within a single withCredentials( …​ ) { …​ } step by doing the following:

1. From the Jenkins home page (i.e. the Dashboard of Jenkins' classic UI), click the name of your Pipeline project/item.

2. On the left, click Pipeline Syntax and ensure that the Snippet Generator link is in bold at the top-left. (If not, click its link.)

3. From the Sample Step field, choose withCredentials: Bind credentials to variables.

4. Click Add under Bindings.

5. Choose the credential type to add to the withCredentials( …​ ) { …​ } step from the dropdown list.

6. Specify the credential Bindings details. Read more above these in the procedure under For other credential types (above).

7. Repeat from "Click Add …​" (above) for each (set of) credential/s to add to the withCredentials( …​ ) { …​ } step.

8. Click Generate Pipeline Script to generate the final withCredentials( …​ ) { …​ } step snippet.


#### 处理参数
```
properties([parameters([string(defaultValue: 'Hello', description: 'How should I greet the world?', name: 'Greeting')])])

node {
    echo "${params.Greeting} World!"
}

```

#### 处理失败：
```
node {
    /* .. snip .. */
    stage('Test') {
        try {
            sh 'make check'
        }
        finally {
            junit '**/target/*.xml'
        }
    }
    /* .. snip .. */
}
```

#### 使用多个代理
```
stage('Build') {
    node {
        checkout scm
        sh 'make'
        stash includes: '**/target/*.jar', name: 'app' 
    }
}

stage('Test') {
    node('linux') { 
        checkout scm
        try {
            unstash 'app' 
            sh 'make check'
        }
        finally {
            junit '**/target/*.xml'
        }
    }
    node('windows') {
        checkout scm
        try {
            unstash 'app'
            bat 'make check' 
        }
        finally {
            junit '**/target/*.xml'
        }
    }
}
```

使用命名参数语法作为Groovy语法中Map的简写，example：
```
// git
git([url: 'git://example.com/amazing-project.git', branch: 'master'])  //map
git url: 'git://example.com/amazing-project.git', branch: 'master'  //named-parameter


// sh
sh([script: 'echo hello'])      //map
sh 'echo hello'                 // named-parameter，只有一个参数可省略参数名  
```


#### 高级脚本管道
Test 阶段并行执行 
```
stage('Build') {
    /* .. snip .. */
}

stage('Test') {
    parallel linux: {
        node('linux') {
            checkout scm
            try {
                unstash 'app'
                sh 'make check'
            }
            finally {
                junit '**/target/*.xml'
            }
        }
    },
    windows: {
        node('windows') {
            /* .. snip .. */
        }
    }
}
```

#### Gitlab 触发
https://docs.gitlab.com/ee/integration/jenkins.html
```
node {
       stage('gitlab') {
             echo 'Notify GitLab'
             updateGitlabCommitStatus name: 'build', state: 'pending'
             updateGitlabCommitStatus name: 'build', state: 'success'
       }
 }
```  

commit status API: https://docs.gitlab.com/ee/api/commits.html#commit-status