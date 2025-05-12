from sub_part.models  import *
from django.core.management.base import BaseCommand
from typing import Any
import random


class Command(BaseCommand):
    help="this command is  inserts post data"

    def handle(self, *args:Any, **options:Any): 
        #delete existing data becoz create slug 
        Post.objects.all().delete()
                
        titles=[
        " Artificial Intelligence (AI)",
            "Machine Learning (ML)",
            "Deep Learning (DL)",
            "Natural Language Processing (NLP)",
            "Computer Vision",
            "Internet of Things (IoT)",
            "Blockchain Technology",
        "    Cybersecurity",
        "    Quantum Computing",
        " Cloud Computing",
        "    Edge Computing " ,   
        "    Big Data Analytics",
        "    Augmented Reality (AR) & Virtual Reality (VR)",
            "5G Technology",
        "   Autonomous Vehicles",
        " Wearable Technology",
        "  Robotics and Automation",
        " Bioinformatics and AI in Healthcare",
        " Ethics in AI",
            "Metaverse",
        ]

        contents=[
            "AI revolutionizes industries through intelligent automation.",
            "Machine learning enables smarter data-driven decision making.",
            "Deep learning enhances neural networks for better predictions.",
            "NLP powers chatbots, translation, and text analysis.",
            "Computer vision improves object detection and image processing.",
            "IoT connects smart devices for seamless data communicat,ion.",
            "Blockchain secures transactions with decentralized digital ledgers.",
            "Cybersecurity safeguards networks from evolving cyber threats.",
            "Quantum computing accelerates complex problem-solving processes.",
            "Cloud computing provides scalable and flexible digital solutions.",
            "Edge computing enables faster real-time data processing.",
            "Big data analytics extracts insights from massive datasets.",
            "AR and VR create immersive digital user experiences.",
            "5G technology enhances speed, connectivity, and network efficiency.",
            "Autonomous vehicles leverage AI for self-driving capabilities.",
            "Wearable technology improves health monitoring and fitness tracking.",
            "Robotics automates industrial processes for improved efficiency.",
            "AI transforms healthcare with advanced disease detection.",
            "Ethical AI ensures fairness, transparency, and responsible usage.",
            "Metaverse merges virtual and physical digital environments.",

        ]

        img_urls=[
            "https://picsum.photos/id/1/800/400",
            "https://picsum.photos/id/2/800/400",
            "https://picsum.photos/id/3/800/400",
            "https://picsum.photos/id/4/800/400",
            "https://picsum.photos/id/5/800/400",
            "https://picsum.photos/id/6/800/400",
            "https://picsum.photos/id/7/800/400",
            "https://picsum.photos/id/8/800/400",
            "https://picsum.photos/id/9/800/400",
            "https://picsum.photos/id/10/800/400",
            "https://picsum.photos/id/11/800/400",
            "https://picsum.photos/id/12/800/400",
            "https://picsum.photos/id/13/800/400",
            "https://picsum.photos/id/14/800/400",
            "https://picsum.photos/id/15/800/400",
            "https://picsum.photos/id/16/800/400",
            "https://picsum.photos/id/17/800/400",
            "https://picsum.photos/id/18/800/400",
            "https://picsum.photos/id/19/800/400",
            "https://picsum.photos/id/20/800/400",
        ]
        
        #insert category id
        categories=category.objects.all()

        for title, content, img_url in zip(titles, contents, img_urls):
            catagory=random.choice(categories)
            Post.objects.create(title=title, content=content, img_url=img_url,category=catagory)

        self.stdout.write(self.style.SUCCESS("completed insert data"))

 