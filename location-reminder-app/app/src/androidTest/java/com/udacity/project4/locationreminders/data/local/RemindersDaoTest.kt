package com.udacity.project4.locationreminders.data.local

import androidx.arch.core.executor.testing.InstantTaskExecutorRule
import androidx.room.Room
import androidx.test.core.app.ApplicationProvider
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.filters.SmallTest
import com.udacity.project4.locationreminders.data.dto.ReminderDTO
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.runBlocking
import org.hamcrest.CoreMatchers.`is`
import org.hamcrest.CoreMatchers.nullValue
import org.hamcrest.MatcherAssert.assertThat
import org.junit.After
import org.junit.Before
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

@ExperimentalCoroutinesApi
@RunWith(AndroidJUnit4::class)
@SmallTest
class RemindersDaoTest {
    @get:Rule
    val instantTaskExecutorRule = InstantTaskExecutorRule()

    private lateinit var database: RemindersDatabase
    private lateinit var dao: RemindersDao

    @Before
    fun initDb() {
        database = Room.inMemoryDatabaseBuilder(
            ApplicationProvider.getApplicationContext(),
            RemindersDatabase::class.java
        ).allowMainThreadQueries().build()
        dao = database.reminderDao()
    }

    @After
    fun closeDb() {
        database.close()
    }

    @Test
    fun saveReminderAndGetById_returnsReminder() = runBlocking {
        val reminder = ReminderDTO("Title", "Description", "Location", 1.0, 2.0, "id-1")

        dao.saveReminder(reminder)

        val loaded = dao.getReminderById("id-1")
        assertThat(loaded?.title, `is`("Title"))
        assertThat(loaded?.location, `is`("Location"))
    }

    @Test
    fun deleteAllReminders_clearsTable() = runBlocking {
        dao.saveReminder(ReminderDTO("Title", "Description", "Location", 1.0, 2.0, "id-1"))

        dao.deleteAllReminders()

        assertThat(dao.getReminders().isEmpty(), `is`(true))
        assertThat(dao.getReminderById("id-1"), nullValue())
    }
}
