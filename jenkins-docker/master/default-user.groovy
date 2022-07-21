import jenkins.model.*
import hudson.security.*

def adminUsername = System.getenv('JENKINS_USER') ?: 'admin'
def adminPassword = System.getenv('JENKINS_PASS') ?: 'admin'

def hudsonRealm = new HudsonPrivateSecurityRealm(false)
def strategy = new GlobalMatrixAuthorizationStrategy()

hudsonRealm.createAccount(adminUsername, adminPassword)
strategy.add(Jenkins.ADMINISTER, adminUsername)

def instance = Jenkins.getInstance()

instance.setSecurityRealm(hudsonRealm)
instance.setAuthorizationStrategy(strategy)

instance.save()
