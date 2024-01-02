def print_examples():
    print("""
        Start STELLA server:    stella serve
        Configure project:      stella config
        Check project:          stella doctor

        login as user:          stella login
        logut as user:          stella logout
        register user:          stella register

        list workspaces:        stella workspace list
        create workspace        stella workspace create myworkspace
        delete workspace:       stella workspace delete myworkspace
        switch workspace:       stella workspace switch defaultWorkspace

        add agent to ws:        stella add spotify
        remove agent from ws:   stella remove spotify
        authenticate agent:     stella auth spotify 

        install agent:          stella install spotify
        uninstall agent:        stella uninstall spotify
        update agent:           stella update spotify
        search for agents:      stella search spotify

        list all agents:        stella status
        stella clean            clean history in chat         
        chat with agents:       stella
    """)