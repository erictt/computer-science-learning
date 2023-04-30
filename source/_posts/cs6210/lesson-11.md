# Lesson 11: Security

## L11a: Principles of Information Security

### Terminologies

- Privacy: Individual control over their information.
- Security: System function that guarantees information properties for users.

### Security Concerns:

- Unauthorized information release: System must prevent unauthorized access to user data.
- Unauthorized modification: System must prevent unauthorized changes to user data.
- Unauthorized denial of use (Denial of Service): System must prevent denial of access to authorized users.

### Levels of Protection

- Unprotected systems: No security measures in place (e.g., MS-DOS).
- All-or-Nothing: Complete isolation between users (e.g., IBM's VM-370).
- Controlled Sharing: Access lists to manage file sharing among users.
- User-Programmed Sharing Controls: Granular access control for different user groups (e.g., Unix file system).
- User-Defined Strings: Custom labels for data classification (e.g., military file classifications).

### Design Principles (Saltzer's):
  
- Economy of Mechanisms: Simple, verifiable security mechanisms.
- Fail-Safe Defaults: Explicitly allow access, default to no access.
- Complete Mediation: No shortcuts in security measures (e.g., full authentication).
- Open Design: Publish design, protect keys, make cracking computationally infeasible.
- Separation of Privilege: Distribute authority among multiple entities (e.g., two keys to open a bank vault).
- Least Privilege: Limit access to the minimum required for tasks (e.g., need-to-know basis).
- Least Common Mechanism: Choose implementation level carefully (e.g., kernel vs. library).
- Psychological Acceptability: Easy-to-use mechanisms with clear user interfaces.

## L11b: Security in Andrew

### Introduction

The Andrew File System (AFS) was developed at Carnegie Mellon University (CMU) to allow the student community to access a central file system from any workstation on campus. Local disks on the workstations served as caches. The vision was for a user to log into any workstation and have their content appear from the central server. This is similar to what cloud computing and mobile devices do today. The Coda file system was also built at CMU with a similar goal.

### Andrew Architecture

![](https://i.imgur.com/1kVT4na.png)

The Andrew System consists of client workstations (called virtues) connected to a local area network that can access servers in a secure environment (called vice).

**Communication between servers is secure**, but **communication between clients and servers is over insecure links and must be encrypted**. The client workstations run a special process called **Venus** for authentication and client caching of files. RPC is used for file transfer and must be secure due to the insecure communication link.

### Encryption Primer

![](https://i.imgur.com/G4DZB9s.png)

There are two families of encryption systems: **private key** and **public key**. 
1. In **private key** systems, the sender and receiver use a **symmetric key** for encryption and decryption. 
2. In **public key** systems, there is a public key for encrypting data and a private key for decrypting it, aka **asymmetric** key pairs. One-way functions are used to convert data into a cyphertext and vice versa. Key distribution is a difficulty with private key systems, which is overcome by public key systems.

### Private Key Encryption System in Action

![](https://i.imgur.com/NLVZcaw.png)

A private key encryption system involves two entities, A and B, exchanging keys (KA and KB) for encrypting and decrypting messages. The sender's identity must be sent in cleartext for the recipient to know which key to use for decryption. The same key is used for both encryption and decryption of a message.

### Challenges for Andrew System & Solution

The Andrew System has some design challenges. These include **authenticating users**, **authenticating servers**, **preventing replay attacks**, and **isolating users**. 

To address these challenges, the Andrew file system uses **secure RPC** as the basis for client-server communication, and **private key cryptosystem for encryption**. Clear text identity of the sender is needed to identify the decryption key. The designers had to find a way to avoid the security hole of overusing username and password for all communication. To address this, they used **ephemeral IDs and keys** for venus-vize communication over insecure links.

The solution that the Andrew file system implemented is to use **usernames and passwords for logging in only**. Once a user is logged in, they use **ephemeral IDs and keys** for venus-vize communication, which is used to establish an RPC session, download and upload files, and access the file system. 

There are three classes of client-server interactions, which are **logging in**, **RPC session establishment**, and **actual file system access**. The **ephemeral IDs and keys** are used for RPC session establishment and file system access during an RPC session.

### Login Process

![](https://i.imgur.com/1zq1663.png)

The login process in the Andrew system involves a virtual workstation communicating securely with the login server, presenting the **username and password**. The login server then returns two tokens: a **secret token** and a **clear token**. The clear token is a data structure that contains a **handshake key(HKC)**, and the secret token is the encrypted clear token with the key that only the server knows. Both the secret and clear tokens are communicated back to the login process by the login server securely over the insecure link.
- The clear token is used to extract the handshake key, 
- The secret token is unique to this login session and is used as the ephemeral client ID. This avoids exposing the username and password too often on the wire.

When the secret token is used as the client ID in future communication between the virtual workstation and the server, the server can decrypt it and extract the associated clear token and handshake key. This is how the identity of the client can be recognized by the server.

For all future communication between the virtual workstation and the server, the handshake key can be used as the private key for establishing a new RPC session. The pair of tokens is stored on the virtual workstation by Venus for the duration of the login session and discarded at the end of the session.

### RPC Session Establishment

In this section, the process of establishing an RPC (Remote Procedure Call) session can be break down into the following steps:

1. **Initiating the RPC session**: Venus, the client-side process, sends the client identity (secret token) and an encrypted cipher containing a random number (Xr) to Vice, the server. The random number is encrypted using the handshake key in the client (HKC), found in the clear token data structure.
	- ![](https://i.imgur.com/aAcnA3a.png)

2.  **Server decrypts the message**: Vice receives the client identity and encrypted cipher. The server decrypts the secret token using its server-side key to obtain the clear token data structure. It then extracts HKC from the clear token data structure and uses it to decrypt the cipher, obtaining the random number Xr.
3. **Server sends a response to the client**: Vice **increments the random number Xr by 1 (Xr+1)** and **generates a new random number Yr.** It encrypts both values using the handshake key (HKS, which is the same as HKC) and sends the encrypted message to Venus.
	- ![](https://i.imgur.com/BpoOkY7.png)

4. **Client verifies the server**: Venus decrypts the received message using HKC and obtains Xr+1 and Yr. By checking if Xr+1 is the expected value, Venus verifies the server's authenticity.
	- ![](https://i.imgur.com/0scuO20.png)

5. **Client sends a message to the server**: Venus increments Yr by 1 (Yr+1), encrypts it with the handshake key HKC, and sends it to Vice.
	- ![](https://i.imgur.com/PWtkLbp.png)


6. **Server verifies the client**: Vice decrypts the received message and checks if the obtained value is Yr+1. This confirms the client's authenticity.
	- ![](https://i.imgur.com/Ti7WJix.png)

7. **Server generates a session key**: To avoid overusing the handshake key, Vice generates a new **session key (SK)** for this RPC session and sends it to Venus encrypted with HKC.
	- ![](https://i.imgur.com/320kgI1.png)

8. **Client extracts the session key**: Venus decrypts the message using HKC, obtaining the session key (SK). This key will be used for **secure communication within the current RPC session**.

![](https://i.imgur.com/Hu043KZ.png)


### Login is a Special Case of Bind

![](https://i.imgur.com/PSYAgB2.png)

Login is a special case of the general bind operation, using the user's password as the handshake key and username as the client ID. The process validates both client and server. After validation, the server returns a pair of tokens - the secret token and the clear token - encrypted using the password as the handshake key. The login process decrypts the message using the password, obtaining the two tokens. Venus stores these tokens for the duration of the login session. The clear token contains the handshake key needed by Venus for establishing RPC sessions, simplifying the rest of the process.

### Putting it all together

1.  Users log in remotely from workstations over insecure links using their username and password and receive a pair of tokens: a secret token and a clear token (first communication between Venus and Vice).
	1. ![](https://i.imgur.com/3P5GieW.png)

2.  Venus establishes an RPC session on behalf of the client using the secret token and handshake key (HKC) (second communication between Venus and Vice). And Venus receives a session key for use in the particular RPC session.
	1. ![](https://i.imgur.com/IHumP3R.png)

3.  Users perform file system operations such as opening, closing, or writing to a file, which require secure RPC calls (third communication between Venus and Vice). Secure RPC calls are made using the secret token as a client ID and the session key as the private key for encryption.
	1. ![](https://i.imgur.com/myC9ByQ.png)

![](https://i.imgur.com/OpIQPEr.png)

- The username and password are exposed only once per login session.
- The handshake key (HKC) is used only for new RPC sessions and is valid for the duration of the login session.
- The session key is used for all the RPC calls during a given RPC session and its duration is the length of that RPC session.

### AFS Security Report Card
![](https://i.imgur.com/zt0dPQn.png)
