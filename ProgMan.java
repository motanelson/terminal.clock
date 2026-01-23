
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.util.*;

public class ProgMan {

    private JFrame frame;
    private JMenuBar menuBar;

    public ProgMan() {
        frame = new JFrame("ProgMan");
        frame.setSize(640, 480);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.getContentPane().setBackground(Color.BLACK);

        menuBar = new JMenuBar();
        menuBar.setBackground(Color.BLACK);
        menuBar.setForeground(Color.WHITE);

        frame.setJMenuBar(menuBar);

        loadMenus("progman.dat");

        JLabel label = new JLabel("Program Manager", SwingConstants.CENTER);
        label.setForeground(Color.GREEN);
        label.setFont(new Font("Courier New", Font.BOLD, 18));
        label.setOpaque(true);
        label.setBackground(Color.BLACK);

        frame.add(label);
        frame.setLocationRelativeTo(null);
        frame.setVisible(true);
    }

    // ---------------- LOAD FILE ----------------

    private void loadMenus(String filename) {
        File file = new File(filename);
        if (!file.exists()) {
            JOptionPane.showMessageDialog(
                frame,
                "progman.dat não encontrado",
                "Erro",
                JOptionPane.ERROR_MESSAGE
            );
            return;
        }

        JMenu currentMenu = null;

        try (BufferedReader br = new BufferedReader(new FileReader(file))) {
            String line;

            while ((line = br.readLine()) != null) {
                line = line.trim();

                if (line.isEmpty())
                    continue;

                // Novo menu
                if (line.startsWith("[") && line.endsWith("]")) {
                    String menuName = line.substring(1, line.length() - 1).trim();

                    currentMenu = new JMenu(menuName);
                    currentMenu.setForeground(Color.WHITE);
                    currentMenu.setBackground(Color.BLACK);
                    currentMenu.setOpaque(true);

                    menuBar.add(currentMenu);
                    continue;
                }

                // Item de menu
                if (line.contains("=") && currentMenu != null) {
                    String[] parts = line.split("=", 2);
                    String text = parts[0].trim();
                    String commands = parts[1].trim();

                    JMenuItem item = new JMenuItem(text);
                    item.setBackground(Color.BLACK);
                    item.setForeground(Color.WHITE);

                    item.addActionListener(e -> executeCommands(commands));

                    currentMenu.add(item);
                }
            }

        } catch (IOException e) {
            JOptionPane.showMessageDialog(
                frame,
                e.getMessage(),
                "Erro",
                JOptionPane.ERROR_MESSAGE
            );
        }
    }

    // ---------------- EXEC COMMANDS ----------------

    private void executeCommands(String commandString) {
        String[] commands = commandString.split(";");

        for (String cmd : commands) {
            cmd = cmd.trim();
            if (cmd.isEmpty())
                continue;

            try {
                new ProcessBuilder("cmd", "/c", cmd).start();
            } catch (IOException e) {
                JOptionPane.showMessageDialog(
                    frame,
                    e.getMessage(),
                    "Erro ao executar",
                    JOptionPane.ERROR_MESSAGE
                );
            }
        }
    }

    // ---------------- MAIN ----------------

    public static void main(String[] args) {
        SwingUtilities.invokeLater(ProgMan::new);
    }
}
