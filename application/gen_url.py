if __name__ == '__main__':
    urls = [f"http://localhost:8080/test?population={i}\n" for i in range(1000, 10_000_000, 5000)]
    with open('urls.txt', 'w') as file:
        file.writelines(urls)
