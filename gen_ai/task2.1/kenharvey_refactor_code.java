import java.util.Scanner;
import java.text.SimpleDateFormat;
import java.util.Arrays;
import java.util.Calendar;

/* Mega Millions are:
 an array of Lottery Tickets,
 an array of Winning Numbers Drawing, and
 an array of Winning Results.
 The comparison of Tickets and Drawings produce Results.
 Lottery Tickets have:
 an array of Lottery Numbers,
 both a starting and an ending date, and
 a name to identify the ticket.
 Lottery Numbers are:
 produced by the Lottery Number Factory
 */

/** Each Lottery Ticket has a set of Purchased Numbers */
class MegaMillions {
    public static final int MAX_PHYSICAL_TICKET_COUNT = 8;
    public static final int MAX_DRAWINGS = 12;
    public static final String ynPrompt = "enter yes or no";
    public static final String[] yesno = { "yes", "no", "y", "n" };

    public static void main(String[] args) {

        Scanner scanner = new Scanner(System.in);
        var ticketFactory = new LotteryTicketFactory(scanner);
        var drawingFactory = new WinningNumbersDrawingFactory(scanner);
        var ticketArray =
                new LotteryTicket[MAX_PHYSICAL_TICKET_COUNT];
        var drawingArray = new Drawing[MAX_DRAWINGS];
        var doAnother = new ValidPromptedWord(scanner, ynPrompt, yesno);
        String answer;

        System.out.println("Lets Play MegaMillions!");
        System.out.println("***********************");
        System.out.println("***********************");
        // TODO give "fill Tickets" and "fill Drawings" to builder classes
        // fill Tickets
        int ticketArrayCount = 0;
        for (int i = 0;
             i < MAX_PHYSICAL_TICKET_COUNT;
             i++) {
            if (i > 0) {
                System.out.printf("> Create new ticket, (number [%d])? ",
                        i+1);
                answer = doAnother.getValidWordAnswer();
                if (answer.equalsIgnoreCase("no") ||
                        answer.equalsIgnoreCase("n")) {
                    System.out.println("Done entering Tickets.");
                    break;
                }
            }
            ticketArray[i] = ticketFactory.getLotteryTicket();
            ticketArrayCount++;
        } // end-for
        // repopulate ticketArray[] null fields with nullLotteryTicket(s)
        for (int i = ticketArrayCount; i < MAX_PHYSICAL_TICKET_COUNT; i++) {
            // System.out.printf("ticketArrayCount == %d\n", ticketArrayCount); //%%
            ticketArray[i] = new nullLotteryTicket();
        }

        // fill Drawings
        int drawingArrayCount = 0;
        for (int i = 0; i < MAX_DRAWINGS; i++) {
            if (i > 0) {
                System .out
                        .printf("> Create new drawing, (number [%d])? ",
                                i + 1);
                answer = doAnother.getValidWordAnswer();
                if (answer.equalsIgnoreCase("no") ||
                        answer.equalsIgnoreCase("n")) {
                    System.out.println("Done entering Drawings.");
                    break;
                }
            }
            drawingArray[i] = drawingFactory.getDrawingResults();
            drawingArrayCount++;
        } // end-for
        // repopulate drawingArray[] null fields with nullDrawing(s)
        for (int i = drawingArrayCount; i < MAX_DRAWINGS; i++) {
            // System.out.printf("drawingArrayCount == %d\n", drawingArrayCount); //%%
            drawingArray[i] = new nullDrawing();
        }

        // TODO try doing .this != null check on quoteResults()
        for(int i = 0; i < MAX_PHYSICAL_TICKET_COUNT; i++) {
            // if (ticketArray[i] != null)   // %% BUGFIX:refactoring
            System.out.printf("i == %d\n", i);  //%%
            ticketArray[i].quoteResults();
        }
        for(int i = 0; i < MAX_DRAWINGS; i++) {
            if (drawingArray[i] != null)
                drawingArray[i].quoteResults();
        }

        int maxPlays = LotteryTicketFactory.MAX_SETS_OF_PLAYS_PER_TICKET;
        var winnerFactory = new WinningPlaysFinder();
        WinningPlay[] winningTickets =
                new WinningPlay[MAX_PHYSICAL_TICKET_COUNT * maxPlays];

        // NOTE winnerFactory returns a set of 5. Put the Nth set of 5 in the correct slot
        //      within the winningTickets[40] array.
        for (int i = 0; i < MAX_PHYSICAL_TICKET_COUNT; i++) {
            // if (ticketArray[i] == null)
            if (ticketArray[i] instanceof nullLotteryTicket)
                continue;
            for (int j = 0; j < MAX_DRAWINGS; j++) {
                // if (drawingArray[j] == null)
                if (drawingArray[j] instanceof nullDrawing)
                    continue;
                var subSet = winnerFactory.getWinningPlays(ticketArray[i], drawingArray[j]);
                System.arraycopy(subSet, 0, winningTickets, maxPlays * i, 5);
                // for (int k = 0; k < maxPlays; k++) {
                //     winningTickets[maxPlays * i + k] = subSet[k];
                // }
            }
        }

        for (int i = 0; i < MAX_PHYSICAL_TICKET_COUNT * maxPlays; i++) {
            if (winningTickets[i] != null)
                winningTickets[i].quoteResults();
        }


        scanner.close();
    }
}

/** Interface used by records: LotteryTicket and Drawing
 TODO : create a version returning a String
 */
interface resultsInterface {
    void quoteResults();
}

/** Interface used by record: LotteryNumberLine
 NOTE both LotteryTicket and Drawing have LotteryNumberLine(s).
 So, to return the number arrays (as arrays)
 from either a LotteryTicket or a Drawing , access
 the LotteryNumberLine(s) possessed by
 the LotteryTicket or Drawing, then call getArray()
 */
interface LotteryLineInterface extends resultsInterface {
    int[] getArray();
}

/** NOTE: Immutable class objects:
 (These were originally records,
 but I want nullObject versions
 derived from these 4
 -- and records are final)

 Immutable class    |  What the class represents
 -------------------|----------------------------------------
 LotteryNumberLine  |  The 5 numbers followed by the Mega
 LotteryTicket      |  Information found on a lottery ticket
 Drawing            |  Results from a bi-weekly lotto drawing
 WinningPlay        |  A winning result, with its information
 */

class LotteryNumberLine implements LotteryLineInterface {
    public static final int LOTTERY_NUMBERS_COUNT = 6;
    private final int n1, n2, n3, n4, n5, Mega;
    public LotteryNumberLine
            (int _n1, int _n2, int _n3, int _n4, int _n5, int _Mega) {
        n1 = _n1; n2 = _n2; n3 = _n3;
        n4 = _n4; n5 = _n5; Mega = _Mega;
    }
    public int[] getArray() {
        return new int[] { n1, n2, n3, n4, n5, Mega };
    }

    public void quoteResults() {
        int[] lottoArray = getArray();
        for (int e = 0; e < LOTTERY_NUMBERS_COUNT - 1; e++) {
            System.out.printf("%3d ", lottoArray[e]);
        }
        String mega = "<"
                + lottoArray[LOTTERY_NUMBERS_COUNT - 1]
                + ">";
        System.out.printf("%4s\n", mega);
    }
}

class LotteryTicket implements resultsInterface {
    protected String name;
    protected LotteryNumberLine[] playLines;
    protected Calendar fromDate;
    protected Calendar toDate;
    protected boolean paidMultiplier;

    public LotteryTicket (String _name, LotteryNumberLine[] _playLines,
                          Calendar _fromDate, Calendar _toDate,
                          boolean _paidMultiplier) {
        name = _name;
        playLines = _playLines;
        fromDate = _fromDate;
        toDate = _toDate;
        paidMultiplier = _paidMultiplier;
    }

    public String getName() {
        return name;
    }
    public LotteryNumberLine[] getPlayLines() {
        return playLines;
    }
    public Calendar getFromDate() {
        return fromDate;
    }
    public Calendar getToDate() {
        return toDate;
    }
    public boolean getPaidMultiplier() {
        return paidMultiplier;
    }

    public void quoteResults() {
        System.out.println("\n==========================================");
        System.out.printf("Lottery Ticket Name: %s\n", name);
        System.out
                .printf("Valid From: %s\n", fromDate.getTime());
        System.out
                .printf("Valid To  : %s\n", toDate.getTime());
        if (paidMultiplier) {
            System.out.println("Multiplier Enabled");
        } else {
            System.out.println("Multiplier Disabled");
        }
        System.out.println("--------------------------------");
        for (int i = 0;
             i < LotteryTicketFactory.MAX_SETS_OF_PLAYS_PER_TICKET;
             i++) {
            if (playLines[i] != null) {
                playLines[i].quoteResults();
            }
        }
        System.out.println("==========================================\n");
    }
}

/** NOTE Keeping class Drawing out of class.
 (instead of inside {@link WinningNumbersDrawingFactory})
 I'm thinking that holding
 a Drawing will prevent timely deallocation of Factory?
 NOTE : so, records which hard code array elements as record
 fields are bad. Lesson learned.
 */
class Drawing implements resultsInterface {
    Calendar winningDate;
    LotteryNumberLine winningNumbers;
    int winningMultiplier;

    public Drawing (Calendar _winningDate,
                    LotteryNumberLine _winningNumbers,
                    int _winningMultiplier) {
        winningDate = _winningDate;
        winningNumbers = _winningNumbers;
        winningMultiplier = _winningMultiplier;
    }
    public Calendar getWinningDate() {
        return winningDate;
    }
    public LotteryNumberLine getWinningNumbers() {
        return winningNumbers;
    }
    public int getWinningMultiplier() {
        return winningMultiplier;
    }
    public void quoteResults() {
        System.out.println("\n==========================================");
        System.out
                .printf("Drawing Results for: %s\n",
                        winningDate.getTime());
        System.out
                .printf("This Week's Multiplier: %d\n",
                        winningMultiplier);
        System.out.println("--------------------------");
        System.out.println("This Week's Winning Numbers:");
        winningNumbers.quoteResults();
        System.out.println("==========================================\n");
    }
}

/** Winning information */
class WinningPlay implements resultsInterface {
    String ticketName;
    Calendar drawingDate;
    LotteryNumberLine playLine;
    LotteryNumberLine drawingLine;
    int normalMatches;
    boolean megaMatched;
    boolean paidMultiplier;
    int multiplier;  // TODO change to winningMultiplier

    public WinningPlay (String _ticketName,
                        Calendar _drawingDate,
                        LotteryNumberLine _playLine,
                        LotteryNumberLine _drawingLine,
                        int _normalMatches,
                        boolean _megaMatched,
                        boolean _paidMultiplier,
                        int _multiplier) {
        ticketName = _ticketName;
        drawingDate = _drawingDate;
        playLine = _playLine;
        drawingLine = _drawingLine;
        normalMatches = _normalMatches;
        megaMatched = _megaMatched;
        paidMultiplier = _paidMultiplier;
        multiplier = _multiplier;
    }
    public String getTicketName() {
        return ticketName;
    }
    public Calendar getDrawingDate() {
        return drawingDate;
    }
    public LotteryNumberLine getPlayLine() {
        return playLine;
    }
    public LotteryNumberLine getDrawingLine() {
        return drawingLine;
    }
    public int getNormalMatches() {
        return normalMatches;
    }
    public boolean getMegaMatched() {
        return megaMatched;
    }
    public boolean getPaidMultiplier() {
        return paidMultiplier;
    }
    public int getMultiplier() {
        return multiplier;
    }
    public void quoteResults() {
        System.out.println("----------------------------------");
        System.out.println("Winner:");
        System.out.printf("<%s> matched %d numbers", ticketName, normalMatches);
        if (megaMatched) {
            System.out.println(", plus the Mega");
        } else {
            System.out.println(", without the Mega");
        }
        System.out.printf("For the drawing held on: %s.\n", drawingDate.getTime());
        System.out.print("The played numbers were: ");
        playLine.quoteResults();
        System.out.print("The winning numbers were:");
        drawingLine.quoteResults();
        if (paidMultiplier) {
            System.out.printf("The week's purchased multiplier was: %d.\n", multiplier);
        } else {
            System.out.println("Multiplier was not purchased");
        }
        System.out.println("----------------------------------");
    }
}

/**
 NOTE null records here are provided to implement nullObject(s) paradigm.
 // Arrays (of compile-time size, or course) frequently don't fill to
 capacity,
 // leaving null elements, and requiring null checks everywhere.
 // Having nullObjects allows for consistent behavior of absent objects.
 // Reference Types requiring this:
 // LotteryNumberLine[MAX_SETS_OF_PLAYS_PER_TICKET] // [5]
 // LotteryTicket[MAX_PHYSICAL_TICKET_COUNT] // [8]
 // Drawing[MAX_DRAWINGS] // [12]
 WinningPlay[MAX_PHYSICAL_TICKET_COUNT*maxPlays] // [8*5 = 40]
 */
// TODO can I place this null-class (bound tightly to LotteryNumberLine) within LotteryNumberLine?

class nullLotteryNumberLine extends LotteryNumberLine {
    public nullLotteryNumberLine() {
        super(0, 0, 0, 0, 0, 0);
    }
    public void quoteResults() {} //do nothing
}

class nullLotteryTicket extends LotteryTicket {
    public nullLotteryTicket() {
        super("", null, null, null, false);
        // System.out.println("\t<<Creating nullLotteryTicket>>");  //%%
    }
    public LotteryNumberLine[] getPlayLines() {
        return new nullLotteryNumberLine[LotteryTicketFactory.MAX_SETS_OF_PLAYS_PER_TICKET];
    }
    public void quoteResults() {
        System.out.println("nada");  //%%
    } //do nothing
}

class nullDrawing extends Drawing {
    public nullDrawing() {
        super(null, null, 0);
    }
    public void quoteResults() {} //do nothing
}

class nullWinningPlay extends WinningPlay {
    public nullWinningPlay() {
        super(null, null, null, null, 0, false, false, 0);
    }
    public void quoteResults() {} //do nothing
}

/** Return a trimmed, non-empty, non-comment string,
 in lower-case,
 via: getAnswer()
 */
// TODO return unaltered strings. Validate using ignoreCase
abstract class Prompt {
    private final String prompt;
    private Scanner scanner;

    public Prompt(Scanner sc, String pr) {
        scanner = sc;
        prompt = pr;
    }

    private void query() {
        System.out.println(prompt);
    }

    public String getAnswer() {
        query();
        String inputLine;
        while (true) {
            inputLine = scanner.nextLine();
            inputLine = inputLine.trim();
            inputLine = inputLine.toLowerCase();
            if (inputLine.isEmpty())
                continue;
            char firstChar = inputLine.charAt(0);
            if (firstChar != '#')
                break;
        }
        return inputLine;
    }
}

/** Return integer array of specified length.
 ie: Length-6 for lotto, Length-3 for calendar/date
 Prompt gets a valid string;
 Here we get a valid set of numbers, using Prompt until we get one.
 "Valid" here simply means the set has the requested number of items.
 */
abstract class ValidPromptedIntegerSet extends Prompt {
    private final int itemCount;

    public ValidPromptedIntegerSet(Scanner scanner,
                                   String prompt,
                                   int countOfItems) {
        super(scanner, prompt);
        itemCount = countOfItems;
    }
    public int[] getValidNumbers() {
        int[] numbers;
        prompt:
        while (true) {
            String response = getAnswer();
            numbers = new int[itemCount];
            String[] allWords = response.split(" ");
            String[] words = new String[allWords.length];
            int current = 0;
            // remove empty string entries
            for (String thisWord : allWords) {
                if (!thisWord.isEmpty()) {
                    words[current] = thisWord;
                    current++;
                }
            }

            if (current != itemCount) continue;
            for (int i = 0; i < itemCount; i++) {
                try {
                    numbers[i] = Integer.parseInt(words[i]);
                } catch (NumberFormatException e){
                    System.out.println("Invalid number string!");
                    continue prompt;
                }
            }
            break;
        }
        return numbers;
    }
}

/** Returns LotteryNumberLine,
 verified as lotto numbers
 via getLotteryNumberLine();
 */
class LotteryNumberFactory extends ValidPromptedIntegerSet {
    private int[] sixNumbers;
    private static final String numPrompt =
            "enter a lottery ticket line";
    private static final int lottoIntFieldCount = 6;

    public LotteryNumberFactory(Scanner sc) {
        super(sc, numPrompt, lottoIntFieldCount);
    }

    private int[] createValidLotteryNumbers() {
        prompt: while (true) {
            sixNumbers = getValidNumbers();
            for (int i = 0; i < lottoIntFieldCount - 1; i++) {
                if (sixNumbers[i] < 1 || sixNumbers[i] > 70) {
                    System.out.print("Invalid Lottery Numbers! : ");
                    System.out.println("(Numbers-range error)");
                    continue prompt;
                }
            }
            if (sixNumbers[lottoIntFieldCount - 1] < 1
                    || sixNumbers[lottoIntFieldCount - 1] > 25) {
                System.out.print("Invalid Lottery Numbers! : ");
                System.out.println("(Mega-range error)");
                continue;
            }
            Arrays.sort(sixNumbers, 0, lottoIntFieldCount - 1);
            // disallow duplicates in the first 5 numbers
            for (int i = 0; i < lottoIntFieldCount - 2; i++) {
                if (sixNumbers[i] == sixNumbers[i + 1]) {
                    // quote();
                    System.out.print("Invalid Lottery Numbers! : ");
                    System.out.println("(duplicates)");
                    continue prompt;
                }
            }
            break;
        }
        return sixNumbers;
    }

    public LotteryNumberLine getLotteryNumberLine() {
        createValidLotteryNumbers();
        return new LotteryNumberLine (sixNumbers[0], sixNumbers[1],
                sixNumbers[2], sixNumbers[3],
                sixNumbers[4], sixNumbers[5]);
    }
}

/** Return a LotteryTicket record
 via getLotteryTicket()
 */
class LotteryTicketFactory {
    Scanner sc;
    public static final int MAX_SETS_OF_PLAYS_PER_TICKET = 5;
    public final String ynPrompt = "Enter yes or no";
    public final String morePrompt = "Enter another line of numbers?";
    public final String multPrompt = "Was the multiplier purchased?";
    public final String[] yesno = { "yes", "no", "y", "n" };
    private LotteryNumberLine[] playLines;
    private Calendar fromDate, toDate; // via ValidPromptedDate
    private String ticketName;
    private boolean multiplier;

    public LotteryTicketFactory(Scanner _sc) {
        sc = _sc;
        playLines = new LotteryNumberLine[MAX_SETS_OF_PLAYS_PER_TICKET];
    }

    private void createLotteryTicket(Scanner sc) {
        String namePrompt = "Name this ticket: ";
        ticketName = new ValidPromptedName(sc, namePrompt)
                .getValidPromptedName();
        System.out.print("Enter the beginning date for this ticket:  ");
        fromDate = new ValidPromptedDate(sc).getValidDate();
        System.out.print("Enter the ending date for this ticket:  ");
        toDate = new ValidPromptedDate(sc).getValidDate();

        var lotto = new LotteryNumberFactory(sc);
        String morePlays;
        int playLineCount = 0;
        var anotherPlay =
                new ValidPromptedWord(sc,
                        morePrompt + " " + ynPrompt,
                        yesno);
        playLines[playLineCount++] = lotto.getLotteryNumberLine();
        for (int i = 1; i < MAX_SETS_OF_PLAYS_PER_TICKET; i++) {
            morePlays = anotherPlay.getValidWordAnswer();
            if (morePlays.equalsIgnoreCase("no") ||
                    morePlays.equalsIgnoreCase("n")) {
                break;
            }
            playLines[i] = lotto.getLotteryNumberLine();
            playLineCount++;
        }
        // repopulate LotteryNumberLine[] null fields with nullLotteryNumberLine(s)
        for (int i = playLineCount; i < MAX_SETS_OF_PLAYS_PER_TICKET; i++) {
            playLines[i] = new nullLotteryNumberLine();
        }

        var askMultiplier =
                new ValidPromptedWord(sc,
                        multPrompt + " " + ynPrompt,
                        yesno);
        String haveMultiplier =
                askMultiplier.getValidWordAnswer();
        multiplier = haveMultiplier.equalsIgnoreCase("y") ||
                haveMultiplier.equalsIgnoreCase("yes");
    }

    public LotteryTicket getLotteryTicket() {
        createLotteryTicket(sc);
        return new LotteryTicket(ticketName, playLines,
                fromDate, toDate, multiplier);
    }
}

/** Returns Drawing record
 via getDrawingResults();
 */
class WinningNumbersDrawingFactory {
    Scanner scanner;
    Calendar drawingDate;
    LotteryNumberLine winningNumbers;
    int multiplier;
    public WinningNumbersDrawingFactory(Scanner sc) {
        scanner = sc;
    }
    public Drawing getDrawingResults() {
        drawingDate = new ValidPromptedDate(scanner).getValidDate();
        winningNumbers =
                new LotteryNumberFactory(scanner).getLotteryNumberLine();
        multiplier =
                new ValidPromptedMultiplier(scanner).getValidMultiplier();
        return new Drawing(drawingDate, winningNumbers, multiplier);
    }
}

/** Return String beginning with a letter */
class ValidPromptedName extends Prompt {
    public ValidPromptedName(Scanner scanner, String prompt) {
        super(scanner, prompt);
    }
    public String getValidPromptedName() {
        String name;
        while (true) {
            name = getAnswer();

            if (Character.isLetter(name.charAt(0))) {
                break;
            } else {
                System.out.println("Name must start with a letter");
            }
        }
        return name;
    }
}

/** Return valid Calendar Object via getValidDate()*/
class ValidPromptedDate extends ValidPromptedIntegerSet {
    private static final String prompt = "Provide a date in (XX-month, XX-day, XXXX-year) format";
    private static final int dateIntFieldCount = 3;
    Calendar c;
    public Calendar getValidDate() {
        c = Calendar.getInstance();
        while (true) {
            int[] numSet = getValidNumbers();
            if (numSet[0] > 12 || numSet[1] > 31 || numSet[2] < 1980
                    || numSet[0] <= 0 || numSet[1] <= 0 || numSet[2] < 0)
                continue;
            numSet[0]--; // months are computed 0-11, but given by the user as 1-12
            c.clear();
            c.set(Calendar.MONTH, numSet[0]);
            c.set(Calendar.DATE, numSet[1]);
            c.set(Calendar.YEAR, numSet[2]);
            if (numSet[0] != c.get(Calendar.MONTH)
                    || numSet[1] != c.get(Calendar.DATE)
                    || numSet[2] != c.get(Calendar.YEAR)) {
                System.out
                        .println("The given Calendar Date does not exist!");
                continue;
            }
            break;
        }
        return c;
    }
    public ValidPromptedDate(Scanner scanner) {
        super(scanner, prompt, dateIntFieldCount);
    }
    public String quoteDate() {
        String formatedDate = new SimpleDateFormat("MM-dd-yyyy").format(c.getTime());
        return formatedDate;
    }
}

/** Return an int from [1..5]
 ..looping until success.
 */
class ValidPromptedMultiplier extends ValidPromptedIntegerSet {
    private static final String prompt =
            "Enter the multiplier for this week:";
    private static final int multIntCount = 1;
    private static final int lowestMultiplier = 2;
    private static final int highestMultiplier = 5;
    private int[] num; // set of 1 number
    public ValidPromptedMultiplier (Scanner scanner) {
        super(scanner, prompt, multIntCount);
    }
    public int getValidMultiplier() {
        while (true) {
            num = getValidNumbers();
            if (num[0] < lowestMultiplier || num[0] > highestMultiplier) {
                System.out.println("Invalid multiplier!");
                continue;
            }
            break;
        }
        return num[0];
    }
}

/** Return the validated string which matches a valid response.
 TODO: This is another factory. I should be able to reuse the
 same Factory for new input.
 TODO: Derive a class that returns a boolean based on y/n input
 */
class ValidPromptedWord extends Prompt{
    private static final int RESPONSE_POOL_SIZE = 10;
    String validResponseArray[] = new String[RESPONSE_POOL_SIZE];
    private String response;
    public ValidPromptedWord(Scanner scanner,
                             String prompt,
                             String[] validResponses) {
        super(scanner, prompt);

        for (int i = 0; i < validResponses.length; i++) {
            validResponseArray[i] = validResponses[i];
        }
    }
    /** Return a valid response.
     Keep trying if the response is invalid.
     */
    public String getValidWordAnswer() {
        while (true) {
            response = getAnswer();
            if (Arrays.asList(validResponseArray).contains(response))
                break; else continue;
        }
        return response;
    }
}

/** Take 1 ticket and 1 drawing, return WinningPlay[maxPlays=5]
 */
class WinningPlaysFinder {
    // private LotteryTicket ticket;
    // private Drawing drawing;
    private WinningPlay[] winningPlaysArr;
    private int megaIdx =
            LotteryNumberLine.LOTTERY_NUMBERS_COUNT - 1;
    private int maxPlays =
            LotteryTicketFactory.MAX_SETS_OF_PLAYS_PER_TICKET;

    public WinningPlaysFinder() {
        winningPlaysArr = new WinningPlay[maxPlays];
    }

    public WinningPlay[] getWinningPlays(LotteryTicket ticket, Drawing drawing) {
        if (drawing instanceof nullDrawing) {
            return new nullWinningPlay[maxPlays];
        }
        var drawingsArray = drawing.getWinningNumbers().getArray();
        // walk ticket lines
        for (int i = 0; i < maxPlays; i++) {

            // if (ticket.getPlayLines()[i] == null) {    //%%
            if (ticket.getPlayLines()[i] instanceof nullLotteryNumberLine) {
                continue;
            }

            var playsArray = ticket.getPlayLines()[i].getArray();
            int matchingNumbersBeforeMega = 0;
            boolean megaMatch = false;

            for (int j = 0;  // walk numbers from line (minus mega)
                 j < megaIdx - 1;
                 j++) {
                if (playsArray[j] == drawingsArray[j]) {
                    matchingNumbersBeforeMega++;
                }
            }
            if (playsArray[megaIdx] == drawingsArray[megaIdx]) {
                megaMatch = true;
            } else {
                megaMatch = false;
            }
            if (matchingNumbersBeforeMega > 2 ||
                    (matchingNumbersBeforeMega == 2 && megaMatch) ||
                    (matchingNumbersBeforeMega == 1 && megaMatch) ||
                    (matchingNumbersBeforeMega == 0 && megaMatch)) {

                winningPlaysArr[i] =
                        new WinningPlay(ticket.getName(),
                                drawing.getWinningDate(),
                                ticket.getPlayLines()[i],
                                drawing.getWinningNumbers(),
                                matchingNumbersBeforeMega,
                                megaMatch,
                                ticket.getPaidMultiplier(),
                                drawing.getWinningMultiplier());
            }
        }
        return winningPlaysArr;
    }
}
