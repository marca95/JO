from ticket.models import Ticket
from django.test import TestCase
from sports.models import Event, Player, Nation, Sport, Stadium
from django.core.exceptions import ValidationError

class TestTicketModels(TestCase):
    def setUp(self):
        self.sport = Sport.objects.create(name="Basketball", description="Un sport")
        self.stadium = Stadium.objects.create(name="Stade de basket", address="123 Rue du sport", available_space=1000)
        self.nation1 = Nation.objects.create(name="USA", nickname="Américains", image="/usa.jpg")
        self.player1 = Player.objects.create(
            first_name="Michael",
            last_name="Jordan",
            nation=self.nation1,
            birth_date="1963-02-17",
            image="/michael_jordan.jpg",
        )

    def test_type_character_on_ticket(self):
        ticket = Ticket.objects.create(nbr_place=5, price=33, formula="quintuple")
        self.assertIsInstance(ticket.nbr_place, int)
        self.assertIsInstance(ticket.price, int)
        self.assertIsInstance(ticket.formula, str)

    def test_length_exceeds_price(self):
        ticket = Ticket(nbr_place=5, price=987654321, formula="quintuple")
        with self.assertRaises(ValidationError):
            ticket.full_clean()  

    def test_min_value_ticket_price(self):
        ticket = Ticket(nbr_place=5, price=-2, formula="quintuple")
        with self.assertRaises(ValidationError):
            ticket.full_clean()

    def test_min_ticket_content_nbr_place(self):
        ticket = Ticket(nbr_place=-1, price=2, formula="quintuple")
        with self.assertRaises(ValidationError):
            ticket.full_clean()

    def test_max_ticket_content_nbr_place(self):
        ticket = Ticket(nbr_place=11, price=2, formula="quintuple")
        with self.assertRaises(ValidationError):
            ticket.full_clean()

    def test_length_exceeds_formula(self):
        formula_limit = "b" * 101  
        ticket = Ticket(nbr_place=5, price=2, formula=formula_limit)
        with self.assertRaises(ValidationError):
            ticket.full_clean()

    def test_cascade_delete_on_event(self):
        event = Event.objects.create(
            date="2025-12-23",
            hour="20:00:00",
            sport=self.sport,
            stadium=self.stadium,
        )
        event.nation.add(self.nation1)
        event.player.add(self.player1)

        self.assertTrue(Event.objects.filter(id=event.id).exists())
        self.assertTrue(self.nation1.events.filter(id=event.id).exists())
        self.assertTrue(self.player1.events.filter(id=event.id).exists())

        event.delete()

        self.assertFalse(Event.objects.filter(id=event.id).exists())
        self.assertTrue(Player.objects.filter(id=self.player1.id).exists())
        self.assertTrue(Nation.objects.filter(id=self.nation1.id).exists())
