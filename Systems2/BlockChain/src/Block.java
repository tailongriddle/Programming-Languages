// Block.java
import java.io.Serializable;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Date;

public class Block implements Serializable { // Implement Serializable
    private static final long serialVersionUID = 1L; // Add a unique ID for serialization
    
    private String data;
    private long timestamp;
    private int nonce;
    private String hash;
    private String previousHash;

    public Block(String data) {
        this.data = data;
        this.timestamp = new Date().getTime();
        this.nonce = 0;
        this.previousHash = "";
        this.hash = calculateBlockHash();
    }

    public Block() {
        this("Genesis Block");
    }

    public String calculateBlockHash() {
        String instanceVarData = data + timestamp + nonce + previousHash;
        MessageDigest myDigest;
        byte[] hashBytes;

        try {
            myDigest = MessageDigest.getInstance("SHA-256");
            hashBytes = myDigest.digest(instanceVarData.getBytes("UTF-8"));
        } catch (NoSuchAlgorithmException | java.io.UnsupportedEncodingException e) {
            throw new RuntimeException(e);
        }

        StringBuffer buffer = new StringBuffer();
        for (byte b : hashBytes) {
            buffer.append(String.format("%02x", b));
        }

        return buffer.toString();
    }

    public String getHash() {
        return hash;
    }

    public void setHash(String hash) {
        this.hash = hash;
    }

    public String getPreviousHash() {
        return previousHash;
    }

    public void setPreviousHash(String previousHash) {
        this.previousHash = previousHash;
    }

    public int getNonce() {
        return nonce;
    }

    public void setNonce(int nonce) {
        this.nonce = nonce;
    }

    @Override
    public String toString() {
        return "Block [data=" + data + ", timestamp=" + timestamp + ", nonce=" + nonce + ", hash=" + hash + ", previousHash=" + previousHash + "]";
    }
}

