from django.test import TestCase
from sports.models import *
from django.db import IntegrityError
from django.core.exceptions import ValidationError

class SportModelsTest(TestCase):
  def setUp(self):
    Sport.objects.create(name="Ping-pong", image="pingpong_image.jpg")
    Sport.objects.create(name="Waterpolo", image="waterpolo_image.jpg")
    
  def test_length_character_string(self):
    sport1 = Sport.objects.get(name="Ping-pong")
    sport2 = Sport.objects.get(name="Waterpolo")
    
    self.assertLessEqual(len(sport1.name), 50)
    self.assertLessEqual(len(sport2.name), 50)    
    
  def test_same_name(self):
    with self.assertRaises(IntegrityError): 
      Sport.objects.create(name="Ping-pong", image="image.jpg")

  def test_same_image(self):
    with self.assertRaises(IntegrityError): 
      Sport.objects.create(name="piscine", image="pingpong_image.jpg")

class StadiumModelsTest(TestCase):
  def setUp(self):
    Stadium.objects.create(name="Stade d'essai", address = "Rue du test, 14", available_space = 10)
    Stadium.objects.create(name="Jean-Paul Seive", address = "Rue du deuxième test, 15", available_space = 10)
    
  def test_length_character_string(self):
    stadium1 = Stadium.objects.get(name="Stade d'essai")
    stadium2 = Stadium.objects.get(name="Jean-Paul Seive")
    
    self.assertLessEqual(len(stadium1.name), 50)
    self.assertLessEqual(len(stadium2.name), 50)    
    
  def test_length_exceeds(self):
    name_limit = 'b' * 51
    address_limit = 'a' * 101
    stadium = Stadium(name= name_limit, address=address_limit, available_space = 20)
    with self.assertRaises(ValidationError):
        stadium.full_clean()
        stadium.save()
    
  def test_same_name(self):
    with self.assertRaises(IntegrityError): 
      Stadium.objects.create(name="Stade d'essai")

  def test_same_address(self):
    with self.assertRaises(IntegrityError): 
      Stadium.objects.create(name='Jean Bonbon', address="Rue du test, 14", available_space=44)
      
  def test_min_value_space_available(self):
    stadium = Stadium(name = "Toto", address = "Rue de l'Adriatique", available_space= -1)
    with self.assertRaises(ValidationError): 
      stadium.full_clean()
      
  def test_type_character_available_space(self):
    stadium = Stadium(name="Stade valide", address="Valid address", available_space='Character')
    with self.assertRaises(ValidationError):
      stadium.full_clean()


class NationModelsTest(TestCase):
  def setUp(self):
    Nation.objects.create(name="Nation", nickname = "Super nation", image = "/image-test.pdg")
    
  def test_length_character_string(self):
    nation1 = Nation.objects.get(name="Nation")
    
    self.assertLessEqual(len(nation1.name), 50)  
    
  def test_length_exceeds(self):
    name_limit = 'b' * 51
    nickname_limit = 'a' * 51
    nation = Nation(name = name_limit, nickname = nickname_limit, image = "/image-test1.pdg")
    with self.assertRaises(ValidationError):
        nation.full_clean()
        nation.save()
    
  def test_same_name(self):
    with self.assertRaises(IntegrityError): 
      Nation.objects.create(name="Nation")

  def test_same_nickname(self):
    with self.assertRaises(IntegrityError): 
      Nation.objects.create(name="Nation2", nickname = "Super nation", image = "/image-test2.pdg")
      
  def test_same_image(self):
    with self.assertRaises(IntegrityError): 
      Nation.objects.create(name="Nation3", nickname = "Super natio2", image = "/image-test.pdg")
      
  def test_type_character(self):
    nation = Nation(name= 'Nation', nickname = "Super nation", image = "/image-test1.pdg")
    self.assertIsInstance(nation.name, str)
    self.assertIsInstance(nation.nickname, str)
    self.assertNotIsInstance(nation.image, str)
    self.assertNotIsInstance(nation.image, int)
    

class PlayerModelsTest(TestCase):
  def setUp(self):
    self.sport = Sport.objects.create(name="Tir au pistolet", description="Le tir est un sport interessant.", image = '/fusil.jpg')
    self.nation = Nation.objects.create(name="Ouzbékistan", nickname="Les Ouzbék", image="/ouzbékistan.jpg")
    self.player = Player.objects.create(first_name= 'Coco', last_name = "Mery", birth_date = "1995-04-03", nation = self.nation ,image="/cocomery.jpg")
    self.player.sports.add(self.sport)
    self.player.save()
    
  def test_length_exceeds(self):
    first_name = 'b' * 51
    last_name = 'a' * 51
    player = Player(first_name= first_name, last_name=last_name, birth_date = "1995-04-03", nation = self.nation ,image="/cocomery.jpg")
    with self.assertRaises(ValidationError):
        player.full_clean()
        player.save()
    
  def test_type_character(self):
    self.assertIsInstance(self.player.first_name, str)
    self.assertIsInstance(self.player.last_name, str)
    self.assertIsInstance(self.player.birth_date, str)
    
  def test_player_name(self):
    self.assertEqual(self.player.first_name, 'Coco')
    self.assertEqual(self.player.last_name, 'Mery')
    
  def test_delete_on_cascade_nation(self):
    self.assertEqual(Player.objects.count(), 1)
    self.nation.delete()
    
    self.assertEqual(Player.objects.count(), 0)
    
  def test_add_sport_on_one_player(self):
    self.sport = Sport.objects.create(name="Tir à la mitrailette", description="Le tir est un sport qui demande de la concentration.", image = '/fusil-assaut.jpg')
    self.player.sports.add(self.sport)
    
    self.assertEqual(self.player.sports.count(), 2)


class EventModelsTest(TestCase): 
  def setUp(self):
    self.sport = Sport.objects.create(name="Tir au pistolet", description="Le tir est un sport intéressant.", image='/fusil.jpg')
    self.nation = Nation.objects.create(name="Ouzbékistan", nickname="Les Ouzbék", image="/ouzbékistan.jpg")
    self.player1 = Player.objects.create(first_name='Coco', last_name="Mery", birth_date="1995-04-03", nation=self.nation, image="/cocomery.jpg")
    self.player2 = Player.objects.create(first_name='Esto', last_name="Mac", birth_date="1995-05-03", nation=self.nation, image="/estomac.jpg")
    self.stadium = Stadium.objects.create(name="Stade d'essai", address="Rue du test, 14", available_space=10)
    self.admin = User.objects.create_user(username='admin', password='adminpassword', first_name='admin1', last_name='admin2', is_superuser=1, email='admin@admin.ad')
    self.event = Event.objects.create(date='2030-01-01', hour='22:22:22', stadium=self.stadium, sport=self.sport, admin=self.admin)

    self.event.nation.add(self.nation)  
    self.event.player.add(self.player1, self.player2)
    
    self.event.save()
    
  def test_delete_on_cascade_stadium(self):
    self.assertEqual(Event.objects.count(), 1)
    self.stadium.delete()
    
    self.assertEqual(Event.objects.count(), 0)
    
  def test_delete_on_cascade_sport(self):
    self.assertEqual(Event.objects.count(), 1)
    self.sport.delete()
    
    self.assertEqual(Event.objects.count(), 0)
    
  def test_delete_set_null_admin(self):
    self.assertEqual(Event.objects.count(), 1)
    self.admin.delete()
    
    self.event.refresh_from_db()
    self.assertIsNone(self.event.admin)
    
  def test_add_players_with_event(self):
    self.player3 = Player.objects.create(first_name= 'Eric', last_name = "Cantona", birth_date = "1995-05-09", nation = self.nation ,image="/eCantano.jpg")
    self.event.player.set([self.player1, self.player2, self.player3])
    
    self.assertEqual(self.event.player.count(), 3)
    
  def test_add_nations_with_event(self):
    self.nation2 = Nation.objects.create(name="Arménie", nickname="Les Arck", image="/armenia.jpg")
    self.event.nation.set([self.nation, self.nation2])
    
    self.assertEqual(self.event.nation.count(), 2)
    