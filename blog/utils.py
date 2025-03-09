# from itsdangerous import URLSafeTimedSerializer
# from flask import current_app

# def generate_verification_token(email):
    # serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    
    # return serializer.dumps(self.email, salt="email_verification")
    
    
# def verify_token(token, expiration=3600):
    # serializer= URLSafeTimedSerializer(current_app["SECRET_KEY"])
    # try:
        # email = serializer.loads(token, salt= "email_verification", max_age= expiration)
    # except:
        # return None
        
    # return email