Secure smart locker management system

The secure smart locker management system is a web-based application that simulates how a real smart locker system would work in an apartment or condominium.

The system allows one user to securely deposit an item into a locker for another user to retrieve later. Instead of leaving items with a security guard, the system provides a controlled, traceable, and secure way to exchange items.

Background & Problem

In many apartments, when residents need to give items to someone but cannot meet in person, they leave the item with a security guard. This method:
- Has no tracking system
- Lacks accountability
- May cause privacy concerns
- Provides no secure access control

Objective
- To design and develop a web-based smart locker management system that simulates real-world secure locker functionality.
- To demonstrate secure item exchange with role based access control

Scope
- Software implementation that can be accessed through website
- Hardware implementation is NOT included

Target Users & Roles
1. Giver - deposit item, generate access credentials for the receiver

Permission: Deposit item
2. Receiver - authenticates into the system, retrieves the item

Permission: Retrieve item
3. Admin - view audit logs, doesn’t have permission to open locker

Permission: View logs

Core Features 
1. User authentication
2. Deposit and retrieves item
3. Logs Tab for admin

Tech Stack

Backend: Python, Flask, SQLite

Frontend: Vue.js


