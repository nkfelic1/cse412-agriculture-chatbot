from geminiClient import GeminiClient


def main():
    client = GeminiClient()

    print('Welcome to Agri! Type in queries related to agriculture. Type "quit" to exit.')

    while True:
        user_input = input('User: ')
        command = user_input.strip().lower().split()

        if not command:
            continue
        if command[0] == 'quit':
            break

        reply = client.call_gemini(user_input)
        print('Agri:', reply)

    print('Thank you for chatting with Agri!')


if __name__ == '__main__':
    main()