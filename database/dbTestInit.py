#### Create the database schema from scratch ####

def dbInit(cursor, cnx):
    print("In db Init")
    cursor.execute("DROP DATABASE IF EXISTS littlelearners;")
    cursor.execute("CREATE DATABASE littlelearners;")
    cursor.execute("use littlelearners;")

    try:
        cursor.execute("CREATE TABLE test (id INT AUTO_INCREMENT UNIQUE NOT NULL, \
                        username VARCHAR(50) NOT NULL, \
                        password VARCHAR(255) NOT NULL, \
                        email_addr VARCHAR(50) UNIQUE, \
                        first_name VARCHAR(50) NOT NULL, \
                        last_name VARCHAR(50) NOT NULL, \
                        PRIMARY KEY (username) \
                        );")
    except:
        print("Error in test creation")
        raise

    try:
        cursor.execute("CREATE TABLE hasUpdate (tab VARCHAR(64), \
                        child INT, \
                        parent INT, \
                        PRIMARY KEY (tab) \
                        );")
    except:
        print("Error in update creation")
        raise
        
    try:
        cursor.execute("CREATE TABLE bubble (id INT AUTO_INCREMENT UNIQUE NOT NULL, \
                       name VARCHAR(50) NOT NULL, \
                       PRIMARY KEY (name) \
                       );")
    except:
        print("Error in bubble creation")
        raise

    try:              
        cursor.execute("CREATE TABLE parent (id INT AUTO_INCREMENT UNIQUE NOT NULL, \
                        username VARCHAR(50) NOT NULL, \
                        password VARCHAR(255) NOT NULL, \
                        email_addr VARCHAR(50) UNIQUE, \
                        first_name VARCHAR(50) NOT NULL, \
                        last_name VARCHAR(50) NOT NULL, \
                        phone VARCHAR(50), \
                        PRIMARY KEY (username) \
                        );")
    except:
        print("Error in parent creation")    
        raise

    try:             
        cursor.execute("CREATE TABLE member_of (id INT AUTO_INCREMENT UNIQUE NOT NULL, \
                        parent_id INT NOT NULL, \
                        bubble_id INT NOT NULL, \
                        PRIMARY KEY (parent_id, bubble_id), \
                        FOREIGN KEY (parent_id) REFERENCES parent(id) ON DELETE CASCADE, \
                        FOREIGN KEY (bubble_id) REFERENCES bubble(id) ON DELETE CASCADE \
                        );")         
    except:
        print("Error in member_of creation")
        raise

    try:
        cursor.execute("CREATE TABLE child (id INT AUTO_INCREMENT UNIQUE NOT NULL, \
                        first_name VARCHAR(50) NOT NULL, \
                        age INT NOT NULL, \
                        raised_hand BOOL NOT NULL, \
                        nav_failed BOOL NOT NULL, \
                        skill_level INT NOT NULL, \
                        parent_id INT NOT NULL, \
                        image VARCHAR(255), \
                        PRIMARY KEY (first_name, age, parent_id), \
                        FOREIGN KEY (parent_id) REFERENCES parent(id) ON DELETE CASCADE \
                        );")
    except:
        print("Error in child creation")          
        raise

    try:
        cursor.execute("CREATE TABLE class (id INT AUTO_INCREMENT UNIQUE NOT NULL, \
                        name VARCHAR(50), \
                        teacher_name VARCHAR(50), \
                        calendar_id VARCHAR(255), \
                        PRIMARY KEY (name, teacher_name) \
                    );")
    except:
        print("Error in class creation")
        raise

    try:
        cursor.execute("CREATE TABLE activity (id INT AUTO_INCREMENT UNIQUE NOT NULL, \
                        name VARCHAR(50) NOT NULL, \
                        class_id INT NOT NULL, \
                        has_macro BOOL, \
                        url VARCHAR(255), \
                        event_id VARCHAR(255), \
                        PRIMARY KEY (name, class_id), \
                        FOREIGN KEY (class_id) REFERENCES class(id) ON DELETE CASCADE \
                    );")
    except:
        print("Error in activity creation")
        raise

    try:
        # print("Add enrolled in")
        cursor.execute("CREATE TABLE enrolled_in (id INT AUTO_INCREMENT UNIQUE NOT NULL, \
                                child_id INT NOT NULL, \
                                class_id INT NOT NULL, \
                                PRIMARY KEY (child_id, class_id), \
                                FOREIGN KEY (child_id) REFERENCES child(id) ON DELETE CASCADE, \
                                FOREIGN KEY (class_id) REFERENCES class(id) ON DELETE CASCADE \
                            );")
    except:
        print("Error in enrolled_in creation")        
        raise

    try:
        cursor.execute("CREATE TABLE schedule_item (id INT AUTO_INCREMENT UNIQUE NOT NULL, \
                                date_time VARCHAR(50) NOT NULL, \
                                duration INT NOT NULL, \
                                activity_id INT NOT NULL, \
                                PRIMARY KEY (date_time, activity_id), \
                                FOREIGN KEY (activity_id) REFERENCES activity (id) ON DELETE CASCADE \
                            );")
    except:
        print("Error in schedule_item creation")     
        raise

    try:         
        
        cursor.execute("CREATE TABLE macro_element (id INT AUTO_INCREMENT UNIQUE NOT NULL, \
                                orderNum INT NOT NULL, \
                                child_id INT NOT NULL, \
                                activity_id INT, \
                                macroName VARCHAR(255), \
                                url VARCHAR(255), \
                                hasInput BOOL, \
                                input VARCHAR(255), \
                                imgPath VARCHAR(255), \
                                img LONGBLOB, \
                                x INT, \
                                y INT, \
                                PRIMARY KEY (orderNum, child_id, macroName), \
                                FOREIGN KEY (child_id) REFERENCES child(id) ON DELETE CASCADE\
                                );")
    except:
        print("Error in macroElement creation")
        raise


    try:
        cursor.execute("CREATE TABLE help_request (id INT AUTO_INCREMENT UNIQUE NOT NULL, \
                            date_time VARCHAR(50) NOT NULL, \
                            msg TEXT, \
                            video_msg BLOB, \
                            child_id INT NOT NULL, \
                            PRIMARY KEY (date_time, child_id), \
                            FOREIGN KEY (child_id) REFERENCES child (id) ON DELETE CASCADE\
                            );")
    except:
        print("Error in help_request creation")  
        raise

    try:                          
        cursor.execute("CREATE TABLE help_response(id INT AUTO_INCREMENT UNIQUE NOT NULL, \
                            date_time VARCHAR(50) NOT NULL, \
                            msg TEXT, \
                            video_msg BLOB, \
                            responder_id INT NOT NULL, \
                            meeting_url VARCHAR(255), \
                            child_id INT NOT NULL, \
                            new BOOL,\
                            PRIMARY KEY (date_time, responder_id), \
                            FOREIGN KEY (responder_id) REFERENCES parent (id) ON DELETE CASCADE, \
                            FOREIGN KEY (child_id) REFERENCES child (id) ON DELETE CASCADE\
                            );")
    except:
        print("Error in help_reponse creation")    
        raise

    try:                        
        cursor.execute("CREATE TABLE input_data (id INT AUTO_INCREMENT UNIQUE NOT NULL, \
                            date_time VARCHAR(50) NOT NULL, \
                            child_id   INT NOT NULL, \
                            mouse_X INT, \
                            mouse_y INT, \
                            keyboard_input TEXT, \
                            PRIMARY KEY (date_time, child_id), \
                            FOREIGN KEY (child_id) REFERENCES child (id) ON DELETE CASCADE\
                            );")
    except:
        print("Error in input_data creation")       
        raise

    try:                     
        cursor.execute("CREATE TABLE log_entry (id INT AUTO_INCREMENT UNIQUE NOT NULL, \
                            child_id INT NOT NULL, \
                            date_time VARCHAR(50) NOT NULL, \
                            navigation_state BOOL, \
                            PRIMARY KEY (child_id, date_time), \
                            FOREIGN KEY (child_id) REFERENCES child (id) ON DELETE CASCADE \
                            );")
    except:
        print("Error in log_entry creation")              
        raise      

    try:                     
        cursor.execute("CREATE TABLE message (id INT AUTO_INCREMENT UNIQUE NOT NULL, \
                            msg VARCHAR(255), \
                            date_time DATETIME NOT NULL, \
                            child_id INT NOT NULL, \
                            parent_id INT NOT NULL, \
                            sender VARCHAR(20) NOT NULL, \
                            PRIMARY KEY (sender, date_time), \
                            FOREIGN KEY (child_id) REFERENCES child (id) ON DELETE CASCADE, \
                            FOREIGN KEY (parent_id) REFERENCES parent (id) ON DELETE CASCADE \
                            );")
    except:
        print("Error in messages creation")              
        raise      