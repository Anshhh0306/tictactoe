from django.shortcuts import render, redirect

USERNAME = "admin"
PASSWORD = "admin"

def check_winner(board):
    wins = [
        (0,1,2), (3,4,5), (6,7,8),
        (0,3,6), (1,4,7), (2,5,8),
        (0,4,8), (2,4,6)
    ]
    for a, b, c in wins:
        if board[a] != "" and board[a] == board[b] == board[c]:
            return board[a]
    if "" not in board:
        return "Draw"
    return None

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username == USERNAME and password == PASSWORD:
            request.session["logged_in"] = True
            request.session["username"] = username
            request.session["board"] = [""] * 9
            request.session["turn"] = "X"
            return redirect("game")
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})
    return render(request, "login.html")

def logout_view(request):
    request.session.flush()
    return redirect("login")

def game_view(request):
    if not request.session.get("logged_in"):
        return redirect("login")

    board = request.session.get("board", [""] * 9)
    turn = request.session.get("turn", "X")
    winner = request.session.get("winner", None)
    
    if request.method == "POST":
        if "reset" in request.POST:
            board = [""] * 9
            turn = "X"
            winner = None
        elif not winner:  # Only allow moves if game is not over
            move = int(request.POST.get("move"))
            if board[move] == "":
                board[move] = turn
                winner = check_winner(board)
                if not winner:  # Only change turn if game is not over
                    turn = "O" if turn == "X" else "X"

    request.session["board"] = board
    request.session["turn"] = turn
    request.session["winner"] = winner

    display_board = list(enumerate(board))

    return render(request, "game.html", {
        "board": display_board,
        "turn": turn,
        "winner": winner,
        "username": request.session.get("username")
    })
