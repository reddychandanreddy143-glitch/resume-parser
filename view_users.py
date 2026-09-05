from database import SessionLocal, User, ResumeRecord

def retrieve_all_data():
    session = SessionLocal()
    try:
        users = session.query(User).all()
        print("=" * 60)
        print(f" TOTAL REGISTERED USERS: {len(users)}")
        print("=" * 60)

        for u in users:
            print(f"\n[User ID: {u.id}] Username: {u.username} | Email: {u.email}")
            print(f"  Account Created: {u.created_at}")
            
            # Retrieve all resumes owned by this user
            user_resumes = session.query(ResumeRecord).filter(ResumeRecord.user_id == u.id).all()
            print(f"  Total Uploaded Resumes: {len(user_resumes)}")
            
            for r in user_resumes:
                print(f"    -> Doc #{r.id}: {r.filename} | Candidate: {r.candidate_name} | Contact: {r.email or 'N/A'}")
        
        print("\n" + "=" * 60)
    finally:
        session.close()

if __name__ == "__main__":
    retrieve_all_data()