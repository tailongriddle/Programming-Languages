// BCNode.java
import java.io.*;
import java.net.*;
import java.util.*;
import java.util.concurrent.CopyOnWriteArrayList;
import java.net.Socket;
import java.net.SocketException;

public class BCNode {
    public ServerSocket serverSocket; // Made public
    public List<Socket> connections = new CopyOnWriteArrayList<>(); // Made public
    public List<ObjectOutputStream> outputStreams = new CopyOnWriteArrayList<>(); // Made public

    private List<Block> blockchain;
    private int difficulty = 5; // Number of leading 0s required for proof of work

    // Constructor initializes blockchain with Genesis Block
    public BCNode(int port, List<Integer> remotePorts) {
        this.blockchain = new ArrayList<>();
        blockchain.add(new Block()); // Genesis block
        initializeServer(port);
        initializeConnections(remotePorts);
    }

    private void initializeServer(int port) {
        try {
            serverSocket = new ServerSocket(port);
            new Thread(new ConnectionHandler(this)).start();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void initializeConnections(List<Integer> remotePorts) {
        for (int remotePort : remotePorts) {
            try {
                Socket socket = new Socket("localhost", remotePort);
                connections.add(socket);
                ObjectOutputStream out = new ObjectOutputStream(socket.getOutputStream());
                outputStreams.add(out);

                // Retrieve blockchain from an existing node
                ObjectInputStream in = new ObjectInputStream(socket.getInputStream());
                List<Block> remoteBlockchain = (List<Block>) in.readObject();
                if (remoteBlockchain != null && remoteBlockchain.size() > blockchain.size()) {
                    blockchain = remoteBlockchain;  // Replace with the longer chain
                }

                new Thread(new ReadHandler(socket, this)).start();
            } catch (IOException | ClassNotFoundException e) {
                e.printStackTrace();
            }
        }
    }


    public synchronized void addBlock(Block block) {
        block.setPreviousHash(blockchain.get(blockchain.size() - 1).getHash());
        mineBlock(block);
        blockchain.add(block);
        broadcastBlock(block, true);  // Broadcast only if block was mined locally
    }


    private void mineBlock(Block block) {
        String prefix = new String(new char[difficulty]).replace('\0', '0');
        while (!block.calculateBlockHash().substring(0, difficulty).equals(prefix)) {
            block.setNonce(block.getNonce() + 1);
            block.setHash(block.calculateBlockHash());
        }
    }

    public void broadcastBlock(Block block, boolean isLocal) {
        if (!isLocal) return;  // Avoid re-broadcasting blocks received from other nodes
        for (ObjectOutputStream out : outputStreams) {
            try {
                out.writeObject(block);   // Send block to connected nodes
                out.flush();              // Ensure the block is sent immediately
                out.reset();              // Reset stream to avoid caching issues
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }


    public boolean validateChain() {
        for (int i = 1; i < blockchain.size(); i++) {
            Block current = blockchain.get(i);
            Block previous = blockchain.get(i - 1);
            if (!current.getHash().equals(current.calculateBlockHash())) return false;
            if (!current.getPreviousHash().equals(previous.getHash())) return false;
            if (!current.getHash().substring(0, difficulty).equals(new String(new char[difficulty]).replace('\0', '0')))
                return false;
        }
        return true;
    }
    
    public void sendBlockchain(ObjectOutputStream out) {
        try {
            out.writeObject(blockchain); // Send the entire blockchain
            out.flush();
            out.reset();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void removeDisconnectedNode(Socket socket) {
        try {
            int index = connections.indexOf(socket);
            if (index >= 0) {
                connections.remove(index);
                outputStreams.remove(index);
                System.out.println("Node on port " + socket.getPort() + " disconnected.");
            }
        } catch (Exception e) {
            System.out.println("Error during node disconnection cleanup: " + e.getMessage());
        }
    }

    @Override
    public String toString() {
        return "BCNode{" +
                "blockchain=" + blockchain +
                '}';
    }

    public List<Block> getBlockchain() {
        return blockchain;
    }
    
    public int getDifficulty() {
        return difficulty;
    }


    public static void main(String[] args) {
        Scanner keyScan = new Scanner(System.in);
        System.out.print("Enter port to start (on current IP): ");
        int myPort = keyScan.nextInt();
        keyScan.nextLine();  // Consume newline after entering port number

        System.out.print("Enter remote ports (current IP is assumed): ");
        String line = keyScan.nextLine();  // Get the list of remote ports as a single line
        List<Integer> remotePorts = new ArrayList<>();
        if (!line.isEmpty()) {
            for (String port : line.split(" ")) remotePorts.add(Integer.parseInt(port));
        }

        BCNode node = new BCNode(myPort, remotePorts);

        while (true) {
            System.out.println("\nNODE on port: " + myPort);
            System.out.println("1. Display Node's blockchain");
            System.out.println("2. Create/mine new Block");
            System.out.println("3. Kill Node");
            System.out.print("Enter option: ");
            
            int in = keyScan.nextInt();
            keyScan.nextLine();  // Consume newline after entering the option

            if (in == 1) {
                System.out.println(node);
            } else if (in == 2) {
                System.out.print("Enter data for new Block: ");
                String data = keyScan.nextLine();  // Read the block data as a string
                Block block = new Block(data);
                node.addBlock(block);
            } else if (in == 3) {
                keyScan.close();
                System.exit(0);
            }
        }
    }
}


