import collections
import logging
import uuid

collections.Iterable = collections.abc.Iterable
 

class FirestoreDBWrapper:
    def __init__(self, firestore_client):
        self.firestore_client = firestore_client 

    def store_user_in_db(self, user_info: dict, uuid) -> None:
        """Stores the user info in Firestore"""
        user_ref = self.firestore_client.collection('users').document(uuid)
        user_ref.set(user_info)

    
    def get_user_uuid_by_email(self, email: str) -> str:
        """Retrieves user uuid from Firestore by email"""
        user_ref = self.firestore_client.collection('users').where('email', '==', email)
        docs = user_ref.get()

        for doc in docs:
            if doc.exists:
                return doc.id

        return None
    
    def get_user_data_by_slug(self, slug: str) -> dict:
        """Retrieves user data from Firestore by slug"""
        user_ref = self.firestore_client.collection('users').document(slug)
        user_data = user_ref.get()

        if user_data.exists:
            return user_data.to_dict()
        else:
            return None   
        
    def get_user_doc_by_email(self, email: str) -> dict:
        """Retrieves user data from Firestore by email."""
        # Query the 'users' collection for documents where the 'email' field matches the provided email
        user_query = self.firestore_client.collection('users').where('email', '==', email)
        docs = user_query.get()

        for doc in docs:
            if doc.exists:
                return doc

        return None
    
    def get_user_data_by_uuid(self, uuid: str) -> dict:
        """Retrieves user data from Firestore by uuid"""
        user_ref = self.firestore_client.collection('users').document(uuid)
        user_data = user_ref.get()

        if user_data.exists:
            return user_data.to_dict()
        else:
            return None
    
    def get_profile_by_slug(self, user_slug: str) -> dict:
        """Retrieves user data from Firestore by slug"""
        user_ref = self.firestore_client.collection('users').where('user_slug', '==', user_slug)
        docs = user_ref.get()

        # Iterate over the query results
        for doc in docs:
            if doc.exists:
                print(doc.to_dict())
                # Return the whole document data
                return doc.to_dict()
        

        # Return None if no document matches the query
        return None

    def get_all_users(self) -> list:
        """Retrieves all users from Firestore"""
        print("attempting to get all users")
        users = self.firestore_client.collection('users').stream()
        print("users:", users)
        print("all collections:", self.firestore_client.collections())
        for collection in self.firestore_client.collections():
            print(collection.id)
        users_list = []
        for user in users:
            print("user:", user.to_dict())
            users_list.append(user.to_dict())
        return users_list
    
    def update_user_info(self, data: dict) -> None:
        """Updates user info in Firestore based on email."""
        email = data.get('email')
        
        # Check if email is provided
        if email is None:
            logging.error("Failed to update user info: 'email' is missing.")
            return

        users_ref = self.firestore_client.collection('users')
        
        # Query for the user document by email
        query_ref = users_ref.where('email', '==', email).limit(1)
        docs = query_ref.stream()

        doc_found = None
        for doc in docs:
            doc_found = doc
            break

        if doc_found:
            # Update the document with new data
            users_ref.document(doc_found.id).update(data)
            logging.info(f"User info updated successfully for: {email}")
        else:
            logging.warning(f"No user found with email: {email}. Unable to update user info.")

    def get_all_students(self) -> list:
        """Retrieves all students from Firestore"""
        students = self.firestore_client.collection('users').where('isStudent', '==', True).stream()
        print(students)
        students_list = []
        for student in students:
            students_list.append(student.to_dict())
        return students_list

    def get_all_mentors(self) -> list:
        """Retrieves all mentors from Firestore"""
        mentors = self.firestore_client.collection('users').where('isMentor', '==', True).stream()
        mentors_list = []
        for mentor in mentors:
            mentors_list.append(mentor.to_dict())
        return mentors_list
    
    def get_all_alumni(self) -> list:
        """Retrieves all alumni from Firestore"""
        alumni = self.firestore_client.collection('users').where('isAlumni', '==', True).stream()
        alumni_list = []
        for alum in alumni:
            alumni_list.append(alum.to_dict())
        return alumni_list
    
    def get_all_meet_me_for(self, meetMeForFilter) -> list:
        """Retrieves all 'meet me for' options from Firestore"""
        meet_me_for_people = self.firestore_client.collection('users').where('meetMeFor', 'array_contains', meetMeForFilter).stream()
        meet_me_for_list = []
        for meet in meet_me_for_people:
            meet_me_for_list.append(meet.to_dict())
        print(meet_me_for_list)
        return meet_me_for_list
    
    def get_all_areas_of_expertise(self, areaOfExpertiseFilter) -> list:
        """Retrieves all areas of expertise from Firestore"""
        areas_of_expertise_people = self.firestore_client.collection('users').where('areasOfExpertise', 'array_contains', areaOfExpertiseFilter).stream()
        areas_of_expertise_list = []
        for area in areas_of_expertise_people:
            areas_of_expertise_list.append(area.to_dict())
        return areas_of_expertise_list
    
    def get_all_skills(self, skillsFilter) -> list:
        """Retrieves all skills from Firestore"""
        skills_people = self.firestore_client.collection('users').where('skills', 'array_contains', skillsFilter).stream()
        skills_list = []
        for skill in skills_people:
            skills_list.append(skill.to_dict())
        return skills_list