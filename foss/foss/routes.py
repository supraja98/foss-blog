def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('log','/login')
    config.add_route('user','/user')
    config.add_route('signup','/signup')
    config.add_route('post','/post')
    config.add_route('view','/view')
    config.add_route('register','/register')
    config.add_route('account','/account')
    config.add_route('postcomment','/postcomment')
    config.add_route('viewcomment','/viewcomment')
    config.add_route('request','/requestcomment')
    config.add_route('adlogin','/adlogin')
    config.add_route('admin','/admin')
    
    
    
    
