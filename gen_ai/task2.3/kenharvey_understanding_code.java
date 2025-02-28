import java.util.*;
import java.text.SimpleDateFormat;

/**
 * MegaMillions is a lottery system that allows users to:
 * - Create lottery tickets with multiple plays
 * - Input winning number drawings
 * - Compare tickets against drawings to determine winners
 */
public class MegaMillions {
    private static final int MAX_TICKETS = 8;
    private static final int MAX_DRAWINGS = 12;
    private static final Scanner scanner = new Scanner(System.in);
    
    public static void main(String[] args) {
        List<LotteryTicket> tickets = new ArrayList<>();
        List<Drawing> drawings = new ArrayList<>();
        
        System.out.println("Welcome to MegaMillions!");
        createTickets(tickets);
        createDrawings(drawings);
        findWinners(tickets, drawings);
    }

    private static void createTickets(List<LotteryTicket> tickets) {
        while (tickets.size() < MAX_TICKETS) {
            System.out.printf("Create new ticket (%d/%d)? (yes/no): ", tickets.size() + 1, MAX_TICKETS);
            if (!confirm()) break;
            tickets.add(LotteryTicketFactory.createTicket(scanner));
        }
    }

    private static void createDrawings(List<Drawing> drawings) {
        while (drawings.size() < MAX_DRAWINGS) {
            System.out.printf("Create new drawing (%d/%d)? (yes/no): ", drawings.size() + 1, MAX_DRAWINGS);
            if (!confirm()) break;
            drawings.add(DrawingFactory.createDrawing(scanner));
        }
    }

    private static void findWinners(List<LotteryTicket> tickets, List<Drawing> drawings) {
        for (LotteryTicket ticket : tickets) {
            for (Drawing drawing : drawings) {
                ticket.checkWinningNumbers(drawing);
            }
        }
    }

    private static boolean confirm() {
        String response = scanner.nextLine().trim().toLowerCase();
        return response.equals("yes") || response.equals("y");
    }
}

/**
 * Represents a lottery ticket with multiple sets of numbers.
 */
class LotteryTicket {
    private final String name;
    private final List<LotteryNumberLine> playLines;
    private final Calendar fromDate;
    private final Calendar toDate;
    private final boolean multiplier;

    public LotteryTicket(String name, List<LotteryNumberLine> playLines, Calendar fromDate, Calendar toDate, boolean multiplier) {
        this.name = name;
        this.playLines = playLines;
        this.fromDate = fromDate;
        this.toDate = toDate;
        this.multiplier = multiplier;
    }

    public void checkWinningNumbers(Drawing drawing) {
        for (LotteryNumberLine playLine : playLines) {
            if (playLine.matches(drawing.getWinningNumbers())) {
                System.out.println("Winning ticket: " + name + " in drawing on " + drawing.getFormattedDate());
            }
        }
    }
}

/**
 * Represents a lottery drawing with winning numbers.
 */
class Drawing {
    private final Calendar date;
    private final LotteryNumberLine winningNumbers;
    
    public Drawing(Calendar date, LotteryNumberLine winningNumbers) {
        this.date = date;
        this.winningNumbers = winningNumbers;
    }
    
    public LotteryNumberLine getWinningNumbers() {
        return winningNumbers;
    }
    
    public String getFormattedDate() {
        return new SimpleDateFormat("MM-dd-yyyy").format(date.getTime());
    }
}

/**
 * Represents a set of lottery numbers.
 */
class LotteryNumberLine {
    private final Set<Integer> numbers;
    
    public LotteryNumberLine(Set<Integer> numbers) {
        this.numbers = new TreeSet<>(numbers);
    }
    
    public boolean matches(LotteryNumberLine other) {
        return numbers.equals(other.numbers);
    }
}

/**
 * Factory class for creating lottery tickets.
 */
class LotteryTicketFactory {
    public static LotteryTicket createTicket(Scanner scanner) {
        System.out.print("Enter ticket name: ");
        String name = scanner.nextLine().trim();
        Calendar fromDate = PromptUtil.getValidDate(scanner, "Enter start date (MM-DD-YYYY): ");
        Calendar toDate = PromptUtil.getValidDate(scanner, "Enter end date (MM-DD-YYYY): ");
        List<LotteryNumberLine> playLines = new ArrayList<>();
        
        do {
            playLines.add(new LotteryNumberLine(PromptUtil.getValidNumbers(scanner)));
            System.out.print("Add another line? (yes/no): ");
        } while (confirm(scanner));
        
        System.out.print("Purchase multiplier? (yes/no): ");
        boolean multiplier = confirm(scanner);
        return new LotteryTicket(name, playLines, fromDate, toDate, multiplier);
    }

    private static boolean confirm(Scanner scanner) {
        String response = scanner.nextLine().trim().toLowerCase();
        return response.equals("yes") || response.equals("y");
    }
}

/**
 * Factory class for creating lottery drawings.
 */
class DrawingFactory {
    public static Drawing createDrawing(Scanner scanner) {
        Calendar date = PromptUtil.getValidDate(scanner, "Enter drawing date (MM-DD-YYYY): ");
        LotteryNumberLine winningNumbers = new LotteryNumberLine(PromptUtil.getValidNumbers(scanner));
        return new Drawing(date, winningNumbers);
    }
}

/**
 * Utility class for handling user input.
 */
class PromptUtil {
    public static Calendar getValidDate(Scanner scanner, String prompt) {
        Calendar calendar = Calendar.getInstance();
        while (true) {
            System.out.print(prompt);
            String[] parts = scanner.nextLine().split("-");
            if (parts.length == 3) {
                try {
                    calendar.set(Integer.parseInt(parts[2]), Integer.parseInt(parts[0]) - 1, Integer.parseInt(parts[1]));
                    return calendar;
                } catch (NumberFormatException ignored) {}
            }
            System.out.println("Invalid date format. Use MM-DD-YYYY.");
        }
    }
    
    public static Set<Integer> getValidNumbers(Scanner scanner) {
        Set<Integer> numbers = new TreeSet<>();
        while (numbers.size() < 6) {
            System.out.print("Enter 6 unique numbers (1-70): ");
            try {
                numbers.addAll(Arrays.asList(scanner.nextLine().split(" ")).stream().map(Integer::parseInt).filter(n -> n > 0 && n <= 70).toList());
            } catch (Exception ignored) {}
            if (numbers.size() != 6) {
                System.out.println("Invalid input. Ensure you enter 6 unique numbers.");
                numbers.clear();
            }
        }
        return numbers;
    }
}


