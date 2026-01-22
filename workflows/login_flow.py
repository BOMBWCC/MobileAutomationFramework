from workflows.base_workflow import BaseWorkflow
from utils.logger import logger

class LoginFlow(BaseWorkflow):
    """
    Workflow for Login scenarios.
    """
    
    def do_login_and_verify(self, username: str, password: str) -> bool:
        """
        Executes the login process and verifies success on Home Page.
        """
        logger.info("Starting Login Workflow...")
        
        # Interact with Login Page
        self.login_page.login(username, password)
        
        # Verify on Home Page
        success = self.home_page.is_welcome_displayed()
        
        if success:
            logger.success("Login Workflow Successful!")
        else:
            logger.error("Login Workflow Failed: Welcome message not found.")
            
        return success