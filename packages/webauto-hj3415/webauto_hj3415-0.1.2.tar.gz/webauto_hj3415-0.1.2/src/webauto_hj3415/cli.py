import argparse
from .codes import ecolian


def ecolian_cli():
    course_dict = {
        'js': ["정선", ],
        'jc': ["제천", ],
        'gs': ["광산", ],
        'yg': ["영광", ],
        'gc': ["거창", ],
        'fav': ["제천", "정선"],
    }
    parser = argparse.ArgumentParser()
    parser.add_argument('course', help=f"Desired course - {course_dict}")
    parser.add_argument('date', help="Desired date : ex - 0417")
    parser.add_argument('time', help="Desired time : ex - 08:30")
    parser.add_argument('--id', help="Site ID", default="hj3415")
    parser.add_argument('--password', help="Site Password", default="piyrw421")

    args = parser.parse_args()

    if args.course in course_dict.keys():
        ecolian.processing(course_dict[args.course], args.date, args.time, args.id, args.password)
    else:
        print(f"The course should be in {course_dict}")


if __name__ == "__main__":
    ecolian_cli()