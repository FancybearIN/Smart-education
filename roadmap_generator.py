def generate_roadmap(topic, score, total):
    if total == 0:
        return ["⚠️ No answers provided. Please complete the quiz to get a personalized roadmap."]

    percentage = (score / total) * 100

    if percentage >= 80:
        level = "Advanced"
    elif percentage >= 50:
        level = "Intermediate"
    else:
        level = "Beginner"

    roadmap = {
        "Python": {
            "Beginner": [
                "✔️ Learn Python syntax, variables, and data types",
                "✔️ Practice loops, conditionals, and functions",
                "✔️ Use platforms like W3Schools or Programiz",
                "✔️ Solve basic problems on HackerRank"
            ],
            "Intermediate": [
                "🚀 Explore OOP concepts, error handling, and file I/O",
                "🚀 Work with external libraries like requests, pandas",
                "🚀 Start with small projects (e.g., calculator, todo app)",
                "🚀 Practice on Leetcode (easy to medium)"
            ],
            "Advanced": [
                "🔥 Master generators, decorators, and async programming",
                "🔥 Dive into web frameworks like Flask or Django",
                "🔥 Build real-world apps (e.g., API, blog system, scraper)",
                "🔥 Contribute to open-source or write technical blogs"
            ]
        },
        "JavaScript": {
            "Beginner": [
                "✔️ Learn JS syntax, variables, functions, and arrays",
                "✔️ Understand how the DOM works",
                "✔️ Practice events and basic interactivity",
                "✔️ Use platforms like freeCodeCamp"
            ],
            "Intermediate": [
                "🚀 Learn ES6+ features (let, const, arrow functions, etc.)",
                "🚀 Understand async JS: callbacks, promises, fetch API",
                "🚀 Build small projects (e.g., quiz app, weather app)",
                "🚀 Explore JS modules and bundlers like Webpack"
            ],
            "Advanced": [
                "🔥 Master React, Vue, or Angular",
                "🔥 Understand design patterns and performance optimizations",
                "🔥 Build full-stack apps using Node.js + frontend framework",
                "🔥 Get familiar with testing and deployment"
            ]
        }
    }

    return roadmap.get(topic, {}).get(level, [f"No roadmap available for topic: {topic}"])
