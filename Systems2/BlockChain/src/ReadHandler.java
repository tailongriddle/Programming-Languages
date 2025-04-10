import java.io.*;
import java.net.Socket;
import java.net.SocketException;

public class ReadHandler implements Runnable {
    private final Socket socket;
    private final BCNode node;

    public ReadHandler(Socket socket, BCNode node) {
        this.socket = socket;
        this.node = node;
    }

    @Override
    public void run() {
        try (ObjectInputStream in = new ObjectInputStream(socket.getInputStream())) {
            while (true) {
                try {
                    Block block = (Block) in.readObject();
                    System.out.println("Received block from network: " + block);

                    System.out.println("Validating block...");
                    if (validateBlock(block)) {
                        System.out.println("Block is valid. Adding to blockchain.");
                        node.getBlockchain().add(block);
                        node.broadcastBlock(block, false); // Avoid re-broadcasting received blocks
                    } else {
                        System.out.println("Invalid block received. Ignoring.");
                    }
                } catch (EOFException | SocketException e) {
                    // Handle disconnection
                    System.out.println("Connection lost with node on port " + socket.getPort());
                    node.removeDisconnectedNode(socket);
                    break;
                } catch (ClassNotFoundException e) {
                    System.out.println("Received an invalid object. Ignoring.");
                }
            }
        } catch (IOException e) {
            System.out.println("Error in input stream: " + e.getMessage());
            node.removeDisconnectedNode(socket); // Clean up the node upon disconnection
        }
    }
    
    private boolean validateBlock(Block block) {
        // Implement block validation logic here based on hash, previous hash, etc.
        // Example stub:
        return true; // Replace with actual validation logic.
    }
}
