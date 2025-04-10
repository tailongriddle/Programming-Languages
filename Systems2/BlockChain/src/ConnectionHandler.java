// ConnectionHandler.java
import java.io.IOException;
import java.io.ObjectOutputStream;
import java.net.Socket;

public class ConnectionHandler implements Runnable {
    private final BCNode node;

    public ConnectionHandler(BCNode node) {
        this.node = node;
    }

    @Override
    public void run() {
        while (true) {
            try {
                Socket socket = node.serverSocket.accept();
                node.connections.add(socket);
                ObjectOutputStream out = new ObjectOutputStream(socket.getOutputStream());
                node.outputStreams.add(out);

                // Send the current blockchain to the newly connected node
                node.sendBlockchain(out);

                new Thread(new ReadHandler(socket, node)).start();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}


